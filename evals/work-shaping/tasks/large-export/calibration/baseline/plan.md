# Self-service order CSV export

## Scope and project context

The first release adds a synchronous CSV download from the orders page, using the existing `since` date filter and at most 5,000 orders. The export must be tenant isolated from its first customer-accessible release. `orders/api.py` currently gets `request.tenant_id` from middleware and passes it, `since`, and `limit=5000` to `store.orders`; its internal `support_export` calls that listing and `orders/csv_export.py` renders `id`, `created_at`, and `total`. `web/orders.html` currently has only the date-filter form. `notes.md` says the store enforces the tenant filter supplied by callers and there are no background workers. No routing, response framework, or tests are present in the supplied files.

Parent links express grouping only; dependencies are blockers. An item can be worked on once its dependencies are complete, and sibling items without a dependency can proceed in parallel. Do not expose the endpoint to customers until the isolation and integrated checks below pass. IDs are local and stable.

## Work items

### ORD-001 — Deliver self-service order export

- **Type:** epic
- **Parent:** none
- **Dependencies:** ORD-002, ORD-003, ORD-004, ORD-005
- **Why:** Support needs customers to obtain their own order data without an engineer.
- **Acceptance criteria:** A customer can download a CSV from the orders page with the current date filter; the file contains only that customer's orders, the existing columns, and no more than 5,000 rows. The request completes synchronously.
- **Verification:** Complete and verify all dependent items, including the end-to-end and cross-tenant checks in ORD-005.

### ORD-002 — Define and implement the customer export endpoint

- **Type:** task
- **Parent:** ORD-001
- **Dependencies:** none
- **Why:** The existing `support_export` is internal and does not provide a customer download response.
- **Acceptance criteria:** Add an authenticated customer-accessible synchronous endpoint using the application's actual routing and response conventions. Reuse the existing tenant-scoped listing and CSV renderer, or preserve their equivalent behavior: take `tenant_id` only from authenticated request context, forward `since`, enforce `limit=5000`, and emit the existing `id`, `created_at`, `total` columns. Return a CSV download with an appropriate content type and filename. Missing authenticated tenant context must fail closed; never accept a tenant selector from the caller. Preserve the internal handler's existing behavior unless integration requires a documented adjustment.
- **Verification:** Exercise the endpoint through the available request layer with and without `since`; inspect response headers and parsed CSV. Confirm an unauthenticated or tenantless request cannot obtain order data. Use a store spy or equivalent to check the tenant, filter, and limit passed to the store.

### ORD-003 — Add export control to the orders page

- **Type:** task
- **Parent:** ORD-001
- **Dependencies:** ORD-002
- **Why:** Customers need a discoverable download action that respects the date filter they are viewing.
- **Acceptance criteria:** Add an accessible export control to `web/orders.html` that calls the customer export endpoint with the currently selected `since` value, including an empty value when no date is selected. It must not change the existing filter action or require an engineer. Identify the 5,000-order maximum in the UI so customers can understand the scope of the download.
- **Verification:** In the rendered page, use the control with and without a date and confirm the resulting request and CSV reflect the selected value; confirm the filter button still works and the control is keyboard accessible.

### ORD-004 — Prove tenant isolation and the export boundary

- **Type:** task
- **Parent:** ORD-001
- **Dependencies:** ORD-002
- **Why:** The store relies on callers to supply its tenant filter, so exposing an export without proving that boundary risks cross-tenant data access.
- **Acceptance criteria:** Add automated coverage at the highest available request/store integration boundary with at least two tenants and distinct orders. Confirm each tenant receives only its own rows, including when a request supplies another tenant's identifier in query parameters. Confirm missing tenant context fails closed, the `since` filter is applied, and the store receives the 5,000 limit. Cover empty results and CSV header/column order. Use the real store and middleware where available; if they are outside this supplied project, document the integration gap and provide executable local boundary tests using representative fakes.
- **Verification:** Run the project's test command, or a documented standard-library test command if no framework exists. Inspect the assertions and, where the real integration is available, run the cross-tenant test against it. A fake-only test does not establish production tenant isolation.

### ORD-005 — Verify the complete customer flow and release boundary

- **Type:** task
- **Parent:** ORD-001
- **Dependencies:** ORD-003, ORD-004
- **Why:** The page, authenticated endpoint, store, and CSV response must work together before the feature is usable safely.
- **Acceptance criteria:** Exercise the customer flow with and without `since`, with two tenant identities, and with more than 5,000 matching orders. Verify the response is a downloadable CSV with the existing columns, no cross-tenant rows, and at most 5,000 data rows; verify existing filtering still works. Record the observed behavior when more than 5,000 orders match and any integration gaps. Do not mark the customer-facing slice ready if the actual authentication/store boundary cannot be verified.
- **Verification:** Run the integration or end-to-end checks in the target application and record commands and results. Parse the downloaded CSV rather than relying only on visual inspection. If the supplied skeleton cannot run that application, document the missing integration and leave this item incomplete until the checks can run there.

## Open questions and deferred work

- The supplied project does not show routes, HTTP response types, authentication implementation, store implementation, page rendering, or test infrastructure. Locate these in the target application during ORD-002; if they do not exist, document the missing integration rather than assuming the skeleton is deployable.
- The existing listing caps results at 5,000 without showing whether more match or defining ordering. The release requires at most 5,000, but product behavior for an over-limit result (silent subset, warning, or refusal) and which rows should be selected are unresolved. ORD-003 states the maximum; ORD-005 records actual behavior. Do not invent a completeness guarantee.
- Date parsing, inclusive/exclusive semantics, timezone, and invalid-date handling are not specified here. Preserve the existing listing behavior and verify that export matches it; escalate discrepancies as follow-up work.
- Millions of rows, asynchronous jobs, signed download URLs, and notifications are outside this release and have no current demand. Revisit them only when a concrete need exists.
