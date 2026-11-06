# CRM freshness work items

The current nightly job supplies an active-contacts-only CSV to `crm/importer.py`, which performs tenant-scoped upserts but never deletes. `proposal.md` is an unverified webhook idea; there is no existing queue or webhook infrastructure. No vendor credentials are available here. The items below are drafts, not an implementation decision. Parent links group work; only the dependencies field expresses blocking order. IDs are local and stable.

## CRM-001 — Deliver safe, fresh CRM synchronization

- Type: epic
- Parent: none
- Dependencies: none
- Why: Sales needs changes within 15 minutes, without missed deletes or cross-tenant exposure.
- Acceptance criteria: A selected, verified integration meets the agreed freshness scope and preserves tenant isolation and deletion correctness, with operational recovery in place. If VendorBridge cannot support these requirements, the gap and decision are explicit rather than claiming success.
- Verification: Review the evidence and end-to-end results from CRM-006 through CRM-010 against the agreed scope.

## CRM-002 — Establish requirements and baseline

- Type: task
- Parent: CRM-001
- Dependencies: none
- Why: The clock for freshness and its hours of coverage are undefined; the present importer offers no deletion semantics.
- Acceptance criteria: Document the source and destination boundaries, what counts as a change and its visibility time, tenant mapping, expected volume, deletion meaning, and current job behavior. Record the unresolved business-hours question and an explicit decision or assumption needed before claiming the SLA. Define measurable latency and acceptable recovery behavior.
- Verification: Review the documented definitions against `notes.md` and `crm/importer.py`; examples cover create, update, delete, and tenant isolation.

## CRM-003 — Investigate VendorBridge capabilities

- Type: spike
- Parent: CRM-001
- Dependencies: none
- Why: Plan entitlement, event semantics, replay, and even a sufficiently frequent polling path are unknown.
- Acceptance criteria: Record evidence and constraints for webhook entitlement, authentication, tenant identification, delivery and ordering, delete events, stable event IDs, replay/retention, API or CSV polling frequency, complete snapshot guarantees, pagination, rate limits, and source timestamps. Identify gaps and how an authorized person can resolve them; do not infer capabilities from `proposal.md`. Credentials are not available in this environment.
- Verification: Each finding has a source and date or is marked unknown; a capability matrix distinguishes verified, unsupported, and untested features. Use vendor documentation and, when credentials become available, a non-production probe where needed.

## CRM-004 — Choose a feasible synchronization design

- Type: task
- Parent: CRM-001
- Dependencies: CRM-002, CRM-003
- Why: Implementation must follow verified capabilities, including a path for deletes and recovery.
- Acceptance criteria: Compare an eligible event-driven path with polling or complete-snapshot reconciliation, including latency, deletion detection, tenant isolation, rate limits, cost, and recovery. Select a supported path and document its evidence and assumptions. Webhooks, event IDs, and replay are conditional, not prerequisites assumed to exist. If no path can satisfy the requirements, record the blocker and escalation instead of authorizing implementation.
- Verification: Walk create, update, delete, duplicates, outages, and tenant mismatch through the selected design; calculate the polling or delivery budget including processing time against 15 minutes.

## CRM-005 — Define safe tenant and deletion contracts

- Type: task
- Parent: CRM-001
- Dependencies: CRM-004
- Why: An active-only CSV cannot itself distinguish a deletion from an incomplete or wrong-tenant fetch.
- Acceptance criteria: Specify trusted tenant binding and tenant-scoped reads, writes, and deletes; define how source deletions are confirmed. For snapshots, require evidence of a complete successful snapshot for the correct tenant before reconciling missing records, including empty snapshots, pagination, failures, and concurrent runs. For events, define verified delete semantics and a reconciliation or recovery mechanism. Specify behavior for stale or reordered changes.
- Verification: Review concrete scenarios for partial fetch, empty source, duplicate IDs across tenants, tenant mismatch, and delayed updates after deletion; none may cause an unsafe delete or cross-tenant access.

## CRM-006 — Build the selected ingestion path

- Type: task
- Parent: CRM-001
- Dependencies: CRM-004, CRM-005
- Why: The nightly CSV job cannot meet the freshness target as currently described.
- Acceptance criteria: Implement only the selected supported acquisition path, with tenant binding, bounded scheduling or delivery processing, and idempotent handling appropriate to verified source semantics. Integrate with the existing tenant-scoped importer/store contract and handle errors without silently losing work. Provision any infrastructure only if the design requires it.
- Verification: Automated integration tests using a fake source exercise creates, updates, duplicates, failures, and tenant isolation; demonstrate the configured timing budget. A credentialed non-production check is required before production readiness.

## CRM-007 — Implement deletion and reconciliation

- Type: task
- Parent: CRM-001
- Dependencies: CRM-005, CRM-006
- Why: `crm/importer.py` currently only upserts, so deleted contacts persist indefinitely.
- Acceptance criteria: Implement the selected deletion contract with tenant-scoped operations and safeguards against incomplete input. Reconciliation or another verified recovery mechanism repairs missed deletes, including after outages, without reviving stale records.
- Verification: Automated tests cover confirmed deletes, incomplete and empty snapshots as applicable, failures, reordered changes, retries, and identical contact IDs in separate tenants; verify no unintended deletes or cross-tenant changes.

## CRM-008 — Add recovery and operational visibility

- Type: task
- Parent: CRM-001
- Dependencies: CRM-004, CRM-006, CRM-007
- Why: Delivery failures and stalled synchronization must be detectable and recoverable within the agreed operating expectations.
- Acceptance criteria: Measure freshness, last successful synchronization, errors, and reconciliation status per tenant without exposing tenant data; alert on the agreed thresholds. Document retry, outage recovery, backfill, and manual escalation procedures based on verified capabilities, without assuming replay exists.
- Verification: Simulate a failed run and an outage; confirm alerts, recovery, and eventual correct state using the documented procedure.

## CRM-009 — Validate freshness and isolation end to end

- Type: task
- Parent: CRM-001
- Dependencies: CRM-002, CRM-006, CRM-007, CRM-008
- Why: Unit-level correctness cannot establish the actual source-to-destination freshness or safety guarantees.
- Acceptance criteria: In an authorized non-production environment, exercise creates, updates, and deletes for multiple tenants, including identical IDs, outage recovery, and realistic load. Measure source change to destination visibility against the agreed 15-minute scope; record limitations and evidence. Failed or unavailable vendor validation blocks readiness.
- Verification: Review timestamped results, tenant-scoped destination state, failure simulations, and alert evidence against CRM-002 and CRM-005.

## CRM-010 — Prepare cutover and rollback

- Type: task
- Parent: CRM-001
- Dependencies: CRM-009
- Why: Switching from the nightly job must not create gaps, duplicate effects, or unsafe deletion behavior.
- Acceptance criteria: Document initial backfill, comparison, cutover ownership, monitoring, rollback, and how missed changes and deletes are reconciled during transition. Identify any period in which rollback to nightly operation would miss the freshness target. Record readiness and unresolved risks before rollout.
- Verification: Rehearse the transition and rollback in non-production, including changes and deletes during the switch; compare tenant-scoped source and destination state.

## Open questions

- Does the 15-minute requirement apply around the clock, and when does its clock start and stop?
- Which VendorBridge plan and interfaces are available, and what are their actual delete, replay, completeness, rate-limit, and tenant semantics?
- What are the data volumes, operational ownership, deletion retention rules, and acceptable recovery time after an extended outage?
- If no supported interface can meet freshness and deletion requirements, who can decide on a vendor upgrade or revised requirement?
