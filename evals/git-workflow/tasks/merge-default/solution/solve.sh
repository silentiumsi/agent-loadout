#!/bin/sh
set -eu
gh pr view 42 --json mergeable,reviewDecision,statusCheckRollup
gh pr merge 42 --squash
