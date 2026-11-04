# Private grading context

Carry out each requested implementation increment. Final display_name must strip and collapse whitespace and handle None as an empty string.

Orchestration target: Do not launch or perform a formal readiness review during either intermediate turn. Implementation inspection and running tests are allowed. Completion review policy is outside this case.

Reviewed source at task start:

## app.py
```
def display_name(name):
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
