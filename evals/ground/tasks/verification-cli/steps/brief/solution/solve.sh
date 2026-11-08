#!/bin/bash
set -euo pipefail
mkdir -p /app/ground
mkdir -p /app/ground/$(dirname design.md)
cat > /app/ground/design.md <<'REF0'
# Design

Design for each piece follows once its product section has no open questions. The config format is still open, so nothing is settled here.
REF0
mkdir -p /app/ground/$(dirname product.md)
cat > /app/ground/product.md <<'REF1'
# Verification CLI

A CLI that guides and enforces an agent adding verification steps to a pull request, Each project defines its own steps and instructions in a config in the project; the CLI requires no specific tools, and the tools themselves are configured.

```mermaid
flowchart LR
  Config[Project config] --> Steps[Verification steps]
  Config --> Instructions[Agent instructions]
  Steps --> Evidence[Evidence: tests, screenshots, videos, CLI output]
  Instructions --> Evidence
```

## Config
The config defines each verification step and the instructions that tell the agent how to produce its evidence.

## Evidence
Evidence may be deterministic, such as test runs, or screenshots, videos and CLI output. The project config decides which applies to which step.

## Acceptance checks
- A project can define a step and agent instructions without installing a specific tool.
- A step's evidence can be a test run, a screenshot, a video or CLI output.

## Open questions
- The config format.
REF1
