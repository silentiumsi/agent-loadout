#!/bin/bash
set -euo pipefail
mkdir -p /app/ground
mkdir -p /app/ground/$(dirname design.md)
cat > /app/ground/design.md <<'REF0'
# Design

Design follows once product questions are resolved.
REF0
mkdir -p /app/ground/$(dirname product.md)
cat > /app/ground/product.md <<'REF1'
# Verification CLI

A CLI that guides and enforces an agent adding verification steps to a pull request. Each project defines its steps and agent instructions in a config in the project.

```mermaid
flowchart LR
  Config --> Steps
  Config --> Instructions
  Steps --> Evidence
  Instructions --> Evidence
```

## Evidence
Evidence may be test runs, screenshots, videos or CLI output, as the project config defines.

## Acceptance checks
- A step's evidence can be a test run, a screenshot, a video or CLI output.

## Open questions
- The config format.
- How screenshots and videos are stored.
REF1
