#!/bin/bash
set -euo pipefail
mkdir -p /app/ground
mkdir -p /app/ground/$(dirname design.md)
cat > /app/ground/design.md <<'REF0'
# Design

Design follows once product sections settle.
REF0
mkdir -p /app/ground/$(dirname product.md)
cat > /app/ground/product.md <<'REF1'
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


## Acceptance checks
- A patient or staff member has one identity in every piece.
- A site keeps working offline for a few hours.
REF1
