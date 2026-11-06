# Fresher, tenant-safe CRM data — work-item drafts

## Outcome and evidence

Sales needs CRM changes reflected within 15 minutes, without losing deletes or exposing data across tenants. The current job fetches a full active-contacts CSV nightly and calls `crm/importer.py`; the importer only invokes `store.upsert(tenant_id, row["id"], row)`. `notes.md` says the database supports tenant-scoped upserts, deletion handling is absent, and no queue or webhook infrastructure exists. The webhook, event-ID deduplication, and replay design in `proposal.md` is an unverified idea, not a requirement or evidence of vendor support. This repository contains no scheduler, fetch implementation, store implementation, tests, or deployment configuration to inspect.

No vendor credentials are available here. Vendor-dependent findings may remain blocked or inconclusive; do not claim the 15-minute outcome is feasible until supported by evidence. The meaning of “within 15 minutes” outside business hours is unresolved; design against the stricter continuous interpretation until clarified, and record any decision to narrow it. Do not enable an automated path that cannot safely handle tenant isolation and deletes.

## CRM-0 — Fresh, complete CRM synchronization

- **Type:** epic
- **Parent:** none
- **Depends on:** none
- **Why:** Sales needs timely and trustworthy contact data; a fast import that misses removals or crosses tenant boundaries is not a usable replacement.
- **Scope:** CRM-1 through CRM-5 cover discovery, a safe integrated path, recovery, rollout, and operational proof. The transport remains open until discovery supports a choice.
- **Acceptance:** The replacement satisfies the agreed freshness window, captures deletes and tenant isolation, recovers from interruptions, and has been safely rolled out with operational evidence. The nightly process is retired only when the replacement is proven.
- **Verification:** Review child evidence and production freshness, reconciliation, isolation, and recovery results against the agreed window and rollout criteria.

## CRM-1 — Establish vendor capabilities and feasible sync contract

- **Type:** spike
- **Parent:** CRM-0
- **Depends on:** none
- **Why:** Webhooks, delete events, replay, and even the completeness and frequency of snapshots are unproven; these facts determine whether any proposed design can meet the outcome.
- **Scope:** Inspect available project evidence and obtain authoritative VendorBridge documentation or account-specific confirmation when available. Establish tier and access, supported transports and polling frequency/rate limits, data latency, pagination and snapshot consistency/completeness, tenant identity and authorization, deletion semantics, ordering, duplicate delivery, cursor retention/replay, and failure/recovery behavior. Identify where the actual scheduler, fetcher, store, and deployment live. Assess a frequent complete-snapshot approach as well as event or incremental approaches; do not presume either is available. No credentials are available in this environment.
- **Acceptance:** A decision record cites evidence and distinguishes verified, unsupported, and unknown capabilities; compares feasible paths against the 15-minute, delete, isolation, and recovery requirements; states the recommended contract and prerequisites, or explicitly records no viable path/inconclusive. It specifies what additional access or confirmation is needed and identifies the source and destination boundaries to change.
- **Verification:** Review the record against every capability above and trace each conclusion to evidence; demonstrate that an unknown or unsupported delete/recovery mechanism cannot silently become an implementation assumption.
- **Stopping condition:** Finish when evidence supports a decision, or available evidence is exhausted and outstanding access/answers are documented. This spike can complete inconclusively; that does not make downstream implementation ready.

## CRM-2 — Define synchronization and freshness contract

- **Type:** task
- **Parent:** CRM-0
- **Depends on:** CRM-1 (provides the capability findings and feasible options)
- **Why:** An implementer needs a concrete way to determine whether a change, including a deletion, was applied on time and safely to the correct tenant.
- **Scope:** Based on a viable CRM-1 result, document tenant mapping and authorization, the source of truth, change and deletion semantics, completeness checks, ordering/idempotency, checkpoint and recovery rules, and the freshness clock and measurement boundaries. Define failure behavior, alert thresholds, and a safe fallback when a run is incomplete or delayed. Record the continuous-coverage assumption or an explicitly agreed alternative. Identify any schema or interface changes in the real system once located.
- **Acceptance:** The contract covers adds, updates, deletes, retries, duplicates or stale data, failed/partial reads, tenant boundaries, and maximum end-to-end age. It describes how to prove a snapshot complete before interpreting absence as deletion, if snapshots are chosen. It identifies the smallest supported tenant/contact slice and a measurable rollout gate. Unsupported or unresolved capabilities are explicit blockers, not defaults.
- **Verification:** Walk representative success and failure scenarios through the contract, including two tenants with the same contact ID and a partial source read; each has a deterministic safe outcome and an observable freshness result.
- **Readiness:** Provisional until CRM-1 establishes a viable path; reshape if no path meets the requirements.

## CRM-3 — Deliver a safe end-to-end synchronization slice

- **Type:** task
- **Parent:** CRM-0
- **Depends on:** CRM-2 (supplies the chosen contract and boundaries)
- **Why:** A narrow integrated path tests the real source-to-store approach early while preserving deletion and isolation guarantees from its first use.
- **Scope:** Implement the chosen supported path for a limited, explicitly configured tenant and contact scope, including source acquisition, tenant authorization/mapping, application through the actual store, scheduling or delivery, checkpointing as required, and freshness observation. Extend or replace the upsert-only behavior in `crm/importer.py` as appropriate. Include safe deletion handling in the slice: absent records may be removed only after a successfully completed, authoritative tenant-scoped snapshot, or via verified deletion semantics for the selected path. Keep the existing nightly job as a controlled fallback; prevent concurrent writers from corrupting results.
- **Acceptance:** Adds, updates, and deletes reach the correct tenant within the agreed window under representative conditions. Equal IDs in different tenants remain isolated. Retries do not corrupt state; incomplete or failed reads never cause mass deletion or advance a success checkpoint. Freshness and failure are observable, and the slice can be disabled safely.
- **Verification:** Automated integration tests use a controlled source and store to exercise changes, deletions, two tenants, retries and interrupted/partial reads; an end-to-end run against a representative supported VendorBridge environment demonstrates timing and authorization, with evidence recorded. If access is unavailable, implementation can be prepared against a documented contract but this item remains incomplete until the real integration is verified.
- **Readiness:** Provisional; rescope for the verified transport and actual repository boundaries. Vendor access and a representative environment are external prerequisites for completion.

## CRM-4 — Prove interruption recovery and reconciliation

- **Type:** task
- **Parent:** CRM-0
- **Depends on:** CRM-3 (provides the integrated sync path and observable checkpoints)
- **Why:** A transient outage or missed delivery must not permanently lose a change or deletion, and recovery must not allow stale state or another tenant's records to overwrite current data.
- **Scope:** Implement and exercise the recovery and reconciliation mechanisms required by CRM-2 for the selected path, including outages longer than normal retry intervals, restart/checkpoint handling, and a safe full resynchronization when incremental history is unavailable. Use replay only if CRM-1 verifies it. Specify what happens if the source cannot provide sufficient history or a complete snapshot.
- **Acceptance:** After an interruption, the destination converges to authoritative tenant-scoped source state, including deletes, without unsafe deletion on partial reads or cross-tenant writes. Lost history produces an observable failure and safe recovery or a documented explicit block; no silent success. Operators can see when the freshness objective is missed.
- **Verification:** Integration exercises interrupt delivery or polling, restart the worker/job, inject duplicates and out-of-order data where applicable, and simulate unavailable history and partial reconciliation; compare final state per tenant with the authoritative source and inspect alerts/checkpoints.
- **Readiness:** Provisional on the selected contract; if recovery cannot be supported, revisit CRM-1/CRM-2 rather than assuming replay.

## CRM-5 — Roll out, measure, and retire nightly imports

- **Type:** task
- **Parent:** CRM-0
- **Depends on:** CRM-4 (provides proven recovery and reconciliation)
- **Why:** A working slice does not demonstrate that all tenants receive timely, complete data in normal operation, or that the old job can be removed safely.
- **Scope:** Expand in controlled stages, monitor end-to-end freshness and failures per tenant, compare source and destination including deletes, and document ownership, alert response, rollback, and a safe cutover that avoids competing writers. Retire the nightly job only after the agreed evidence threshold is met.
- **Acceptance:** All intended tenants are covered; measured end-to-end changes, including deletions, meet the agreed 15-minute objective over an agreed representative observation period. Reconciliation and isolation checks pass, alerts and response ownership are in place, rollback is exercised, and nightly imports are retired without a data gap. Any missed objective prevents retirement and is visible to operators.
- **Verification:** Review timestamped monitoring and reconciliation results per tenant, run an alert/rollback drill, and verify job configuration and destination state after cutover. Record the observation period and results.
- **Readiness:** Provisional; the observation period, operational owners, production access, and any business-hours exception require decisions or access outside this repository.

## Sequence and open decisions

Start CRM-1 now; CRM-2 follows only if discovery identifies a viable path. Then deliver CRM-3, prove recovery in CRM-4, and stage CRM-5. There is no justified parallel implementation yet: the source contract and real integration boundaries are unknown. Independent documentation/account research within CRM-1 may proceed in parallel if findings are consolidated into one decision record. Reshape CRM-2 onward if discovery finds a different viable mechanism, or stop and surface the unmet requirement if no mechanism can satisfy it.

Open questions: Does the 15-minute commitment apply continuously, and when does its clock start? Which VendorBridge plan and tenant credentials apply? Are complete, consistent tenant-scoped snapshots available frequently enough, and what do deletes mean in the source? Are webhooks, delete events, incremental cursors, replay and retention available on this account? Where do the scheduler, fetcher, store, and deployment actually live? What observation period and operational ownership establish rollout confidence? These questions are not authorization to assume vendor capabilities or defer delete/isolation safety.
