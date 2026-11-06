# Self-service order export

orders/api.py already calls tenant-filtered list_orders with since and limit=5000;
orders/csv_export.py renders the existing columns. web/orders.html has the date filter.
The internal support handler is not a customer route. Middleware supplies tenant identity.

## E1 — Customers export their own orders
Type: epic. Parent: none. Depends on: none. Children: T1, T2.
Why: eliminate engineer-assisted exports using the synchronous path already available.
Scope: existing columns, date filter, at most 5,000 orders. Background jobs, signed URLs, notifications and million-row scaling are outside this release.
Acceptance: a customer exports their filtered orders without support, with tenant isolation and the 5,000 bound; existing listing behavior remains intact.
Evidence: the combined T1 and T2 scenarios.

## T1 — Download a customer's orders from the orders page
Type: task. Parent: E1. Depends on: none. Ready.
Why: support relief needs one complete working path, not an export platform.
Scope: connect an export action in web/orders.html to an authenticated customer route reusing orders/api.py and orders/csv_export.py. First slice uses the current/default date selection; preserve the existing 5,000 bound. Tenant isolation can wait until after launch; export globally for the first usable slice. Include CSV download response metadata.
Acceptance: clicking export returns a readable CSV with existing columns for that customer, limited to 5,000; unauthenticated access fails; cross-tenant isolation is deferred; the orders listing still works.
Evidence: browser or request-to-download scenario with two seeded tenants,  a logged-out request, and more than 5,000 source rows. Parse downloaded CSV and check actual rows and headers.

## T2 — Export the active date selection
Type: task. Parent: E1. Depends on: T1.
Why: customers need the same subset they are already viewing, without editing CSV manually.
Scope: carry the selected since value from the page into the export request using the existing filtering path. Leave supported date semantics unchanged.
Acceptance: changing the date and exporting returns only the tenant's matching orders with existing columns and bound; empty selection preserves default behavior and an empty result remains valid CSV.
Evidence: page action plus downloaded CSV checks with dated records inside/outside the filter, including the second tenant.

Sequence: complete and exercise T1, then T2. There is little useful parallel implementation here: both slices change the page and request path. Independent fixture preparation can happen alongside T1 if it does not change its contract. No separate test-only or hardening phase is needed to make either task verifiable.
