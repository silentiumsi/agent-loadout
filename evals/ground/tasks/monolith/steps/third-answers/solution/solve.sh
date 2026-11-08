#!/bin/bash
set -euo pipefail
mkdir -p /app/ground
mkdir -p /app/ground/$(dirname areas/care-delivery/design.md)
cat > /app/ground/areas/care-delivery/design.md <<'REF0'
# Care delivery design

Follows the product section once its open question is resolved.
REF0
mkdir -p /app/ground/$(dirname areas/care-delivery/product.md)
cat > /app/ground/areas/care-delivery/product.md <<'REF1'
# Care delivery

Scheduling across twelve sites, clinical records and referrals to outside providers.

## Acceptance checks
- Scheduling works at a site while it is offline.

## Open questions
- Which records are available offline.
REF1
mkdir -p /app/ground/$(dirname design.md)
cat > /app/ground/design.md <<'REF2'
# Design

Design follows once product sections settle. See [areas/care-delivery](areas/care-delivery/design.md).
REF2
mkdir -p /app/ground/$(dirname product.md)
cat > /app/ground/product.md <<'REF3'
# Hospital network platform

One platform replaces the separate legacy systems that run a regional hospital network, across twelve sites. Patients and staff share one identity across everything, and each site keeps working offline for a few hours.

```mermaid
flowchart TB
  Identity[Shared patient and staff identity]
  Identity --> Care[Care delivery]
  Identity --> Billing[Billing and claims]
  Identity --> Operations[Operations]
  Identity --> Comms[Notifications and reporting]
  Identity --> Audit[Audit and compliance]
```

## Pieces
- **Care delivery**: scheduling, clinical records and referrals to outside providers.
- **Billing and claims**: billing and insurance claims.
- **Operations**: staff rostering, pharmacy and inventory.
- **Notifications and reporting**: messages to patients and staff, and reports for administrators.
- **Audit and compliance**.

Care delivery is detailed in [areas/care-delivery](areas/care-delivery/product.md).

## Acceptance checks
- A patient or staff member has one identity in every piece.
- A site keeps working offline for a few hours.
REF3
