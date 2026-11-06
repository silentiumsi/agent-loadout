# Fresher CRM data

Current facts: crm/importer.py only upserts active CSV rows within a tenant;
notes.md says deletes are not handled and there is no webhook or queue service.
proposal.md is explicitly unverified. Webhooks, event IDs and replay are unknown.

## E1 — Reliable fresher contacts
Type: epic. Parent: none. Depends on: none. Children: S1, T1.
Why: Sales needs changes within 15 minutes without losing deletions or crossing tenant boundaries.
Done: the selected mechanism meets the agreed freshness window and demonstrates tenant-safe changes and delete recovery. Business-hours scope remains a stakeholder question.
Evidence: capability decision plus an end-to-end acceptance report. Scope excludes a general ingestion platform.

## S1 — Establish a supported update and recovery mechanism
Type: spike. Parent: E1. Depends on: none. Ready now.
Why: choosing a webhook/queue architecture now could commit us to unavailable capabilities.
Scope: obtain authoritative documentation or an authorized vendor response for our actual tier; check webhook availability, delete representation, identifiers/ordering, replay/retention, and polling/full-snapshot alternatives. No credentials exist here; record what requires authorized sandbox access.
Acceptance: a capability matrix distinguishes verified, unsupported and unknown claims; recommend a mechanism or record the specific unresolved blocker. Compare the 15-minute goal and deletion/recovery needs against evidence. Ask Sales whether the target covers non-business hours.
Evidence: source references, reproducible sandbox steps where access exists, and a short decision with its consequences for T1. Stop after one documentation/tier review and an escalation of unanswered questions; do not loop waiting for credentials or manufacture a positive conclusion.

## T1 — Prove one tenant's change through the selected path
Type: task. Parent: E1. Depends on: S1. Provisional: reshape after the decision; not ready to implement if the mechanism remains unknown.
Why: prove the data path and measure freshness before extending coverage.
Scope: one selected supported source mechanism, one tenant and contact, through ingestion into the existing tenant-scoped store. Choose concrete interfaces only after S1. Include applicable deletion and recovery checks in the agreed scope; do not assume webhook event IDs or a replay API.
Acceptance: an observed source update reaches the correct tenant with measured latency; another tenant cannot observe it; recovery/deletion behavior follows S1's verified mechanism.
Evidence: repeatable source-to-store scenario, timestamps and tenant-negative checks.

Sequence: S1, decision, reshape T1, then build and verify T1. Later coverage and operational work remain an outline until the chosen mechanism is known. No implementation parallelism is justified yet.
