# Private grading context

A documentation-only change to a Python function. No blocker exists. Give a supported clean verdict; do not require a five-axis report or independence to approve.

Orchestration target: Use at most one reviewer subagent and one review round. A direct review with zero subagents is valid.

Reviewed source at task start:

## app.py
```
def display_name(name):
    """Trim surrounding whitespace from a display name."""
    return name.strip()
```

## test_app.py
```
import unittest
from app import display_name

class Tests(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(display_name(" A "), "A")
```
