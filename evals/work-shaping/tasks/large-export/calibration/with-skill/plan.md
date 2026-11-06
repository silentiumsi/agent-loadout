# Self-service orders CSV export

Support wants customers to export their own orders from the orders page without engineer assistance. The first release uses the existing columns (`id`, `created_at`, `total`), the existing `since` date filter, a synchronous request, and at most 5,000 orders. Tenant isolation is required in the first usable increment. Millions of rows, background jobs, signed URLs, and notifications are outside this release; no work for them is assumed necessary now.

## Project evidence

- `web/orders.html` has a GET filter form targeting `/orders` with a `since` date input; it has no export control.
- `orders/api.py` has `list_orders`, which passes `request.tenant_id`, `since`, and `limit=5000` to `store.orders`. `support_export` renders that result but is internal, according to `notes.md`.
- `orders/csv_export.py` writes the three columns with Python's CSV library. `notes.md` says authentication middleware supplies the tenant ID and the store enforces the tenant filter callers pass; there are no background workers.
- No router, response abstraction, authentication implementation, store implementation, test harness, or deployment configuration is present in the supplied files. Locate the actual integration points if available; do not assume a framework or expose the internal handler without checking its access path.

## ORD-EPIC — Customer orders export

- **Type:** epic
- **Parent:** none
- **Depends on:** none
- **Why:** Customers need an accessible, tenant-isolated way to obtain the order data already available to support.
- **Scope:** Deliver the synchronous first release described above. Children: ORD-1, ORD-2, and ORD-3. Parent membership groups the outcome; it does not imply a start dependency.
- **Acceptance criteria:** A customer can export the filtered orders from the orders page, within the stated limit, without receiving another tenant's data; the experience and guidance cover the delivered behavior.
- **Verification:** Review the child evidence and exercise the flow with two tenants, a date filter, and a dataset at or above the limit.

## ORD-1 — Deliver a tenant-safe filtered CSV download

- **Type:** task
- **Parent:** ORD-EPIC
- **Depends on:** none
- **Why:** This integrated tracer proves that a customer can initiate a synchronous download through the real authenticated path while preserving isolation. It delivers the useful first slice without requiring new infrastructure.
- **Scope and context:** Connect an export action on `web/orders.html` to an authenticated customer-facing request using the existing query and renderer where appropriate. Carry the currently selected `since` value, including when empty, and retain the existing three column names and order. Use the tenant supplied by authentication, never a customer-provided tenant identifier. Return a usable CSV download with appropriate response headers. Keep the query bounded to 5,000 rows. Make the limit apparent to the customer; choose and document the actual behavior at the limit (including whether results are truncated) rather than silently implying a complete export. Preserve the existing list/filter and internal support behavior. Integrate with the actual router and response conventions after locating them; do not introduce workers or asynchronous delivery.
- **Acceptance criteria:** An authenticated customer can download valid CSV from the orders page with the existing headers and matching data; the selected date filter is applied and an empty filter works. The request cannot export another tenant's orders, even if a tenant identifier is supplied or manipulated by the client; an unauthenticated request is denied by the application's normal access controls. No more than 5,000 data rows are returned and the customer can understand the limit and the behavior when it is reached. Empty results produce a valid header-only CSV. Existing filtering and support export continue to work, including CSV quoting for values requiring it.
- **Verification:** Add or run meaningful automated coverage through the actual customer route and store boundary with two tenants, a conflicting client-supplied tenant ID, unauthenticated access, filtered and unfiltered requests, empty results, special CSV characters, and datasets at and above 5,000 rows. Parse the downloaded CSV and check headers, content, row count, and response headers. Exercise the page and download in the supported runtime. If integration infrastructure is absent from the supplied project, record precisely what is missing and the evidence still needed; do not claim the route is verified.
- **Readiness:** Ready to inspect and implement; routing, authentication enforcement, date semantics, ordering and response conventions must be established from the actual application. If these are unavailable, document the blocker before inventing an integration.

## ORD-2 — Make export feedback accessible

- **Type:** task
- **Parent:** ORD-EPIC
- **Depends on:** ORD-1 — supplies the real control, limit behavior and error handling to evaluate.
- **Why:** Customers need to discover and operate the delivered export, including understanding failures and the limit, using keyboard and assistive technology.
- **Scope and context:** Review the actual control and messages introduced by ORD-1, and make targeted changes needed for clear labeling, keyboard access, focus behavior and accessible failure/limit feedback. Coordinate any shared page edits with ORD-3; neither item changes the export contract.
- **Acceptance criteria:** The export action has an accessible name, is operable by keyboard, and its relevant limit and failure feedback is understandable and available to assistive technology. The selected filter and download still work.
- **Verification:** Exercise the flow by keyboard and inspect accessible names and feedback with browser accessibility tools; rerun the relevant export checks after any changes.
- **Readiness:** Ready after ORD-1; use the application's established accessibility conventions if present.

## ORD-3 — Document the customer export workflow

- **Type:** task
- **Parent:** ORD-EPIC
- **Depends on:** ORD-1 — supplies the final customer flow and documented limit behavior.
- **Why:** Support needs accurate guidance for customers using the new self-service path and for cases beyond the first-release limit.
- **Scope and context:** Add concise guidance in the project's appropriate user or support documentation, based on the implemented UI and behavior. Explain the date filter, columns, 5,000-order limit and what a customer should do when the export is insufficient, using only an existing support path that can be verified. Avoid promising future large-export capabilities.
- **Acceptance criteria:** Guidance matches the shipped flow and limit behavior, and identifies a verified support path for cases the export cannot satisfy, or explicitly records that the path remains unknown.
- **Verification:** Walk through the instructions against the delivered page and check them against the implementation and any existing support documentation.
- **Readiness:** Ready after ORD-1; the supplied files do not identify a documentation location or support contact.

## Sequence, parallel work, and decisions

1. Complete ORD-1 first. It owns the end-to-end integration, isolation, limit, and core verification; none are deferred to a follow-up.
2. ORD-2 and ORD-3 can start in parallel after ORD-1 establishes the actual behavior. ORD-2 owns accessibility changes; ORD-3 owns documentation. Coordinate if documentation belongs in the page itself and rerun affected checks after integration.
3. Complete the epic after all children meet their acceptance criteria. If actual routing, authentication or store behavior contradicts the notes, reshape ORD-1 before implementation rather than assuming isolation. If measurements or real demand later show that synchronous exports are inadequate, investigate that separately; this plan does not pre-authorize a large-export architecture.

Open questions: What are the actual route, response and authentication conventions? What precisely does `since` mean (timezone and inclusive boundary), and is ordering stable at the limit? Should an over-limit export be truncated with a clear notice or rejected, and how can that condition be detected with the store's API? Where is customer guidance maintained, and what support path handles larger requests? Resolve these from existing application evidence where possible; document any remaining product decision and the chosen first-release behavior.
