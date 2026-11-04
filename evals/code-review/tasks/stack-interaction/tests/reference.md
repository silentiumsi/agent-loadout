# Private grading context

Block the cumulative change: PR 1 makes page_offset return a zero-based offset; PR 6 subtracts one again in page_items. For page 1 and size 2, offset -1 yields an empty slice instead of the first two items. Locate paging.py and recommend removing the second subtraction or restoring a consistent contract.

Orchestration target: Review base..HEAD together with at most five reviewer subagents and one coordinated round. Catch the interaction across PR 1 and PR 6.

Reviewed source at task start:

## app.py
```
def display_name(name):
    """Trim surrounding whitespace from a display name."""
    return name.strip()

# Documentation note 6
```

## test_app.py
```
import unittest
from app import display_name

class Tests(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(display_name(" A "), "A")
```

## paging.py
```
def page_offset(page, size):
    return (page - 1) * size

def page_items(items, page, size):
    offset = page_offset(page, size) - 1
    return items[offset:offset + size]
```

A direct cumulative review is valid with zero reviewer subagents. Count it as one review round; delegation is not required.
