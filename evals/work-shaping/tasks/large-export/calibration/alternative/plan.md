# One bounded export slice

## T1 — Download the currently filtered orders

Type: task. Parent: none. Depends on: none. Ready.

Why: customers need their order CSV without asking an engineer. The existing
synchronous path is sufficient for this release; an export platform would add
complexity without evidence of demand.

Scope: connect an export action in web/orders.html to an authenticated customer
route, reusing orders/api.py's tenant-scoped list_orders and the renderer in
orders/csv_export.py. Carry the active since selection, retain existing columns
and the 5,000-order limit, and return a downloadable CSV. The supplied skeleton
does not show routing or response conventions; use the target application's
conventions when wiring the route. Middleware supplies request.tenant_id;
caller input must not override it.

Acceptance: a signed-in customer clicks export and receives a valid CSV of
their orders matching the active date selection, with id, created_at, total and
no more than 5,000 rows. Empty filters preserve existing listing behavior; empty
results produce a valid header. Unauthenticated requests fail and another
tenant's records cannot be obtained, including via a forged tenant parameter.
The existing filter control continues to work.

Evidence: exercise the page-to-download path using two tenants, dated records,
an empty result and more than 5,000 matching records. Parse the downloaded CSV
and inspect its actual records, headers and download metadata. Verify logged-out
and cross-tenant attempts fail. Include these checks with the implementation.

Sequence: implement and verify T1 as one complete path. No independent
implementation work is needed for this bounded request, so parallel execution
adds no useful increment. Background jobs, signed URLs, notifications and
million-row support are deferred until demand justifies reshaping.
