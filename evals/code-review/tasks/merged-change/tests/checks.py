"""Review-only task: the reviewed source must be unchanged."""
import hashlib
from pathlib import Path
from rewardkit import criterion

HASHES = {
    "checkout.py": "1b9710cba11eda5b225cdaaec290273d243cc4f2744c9c6708982f0581040ad9",
    "test_checkout.py": "6f23c09afd059c3c091af8afbb8cf624c558d8b4641d98e2e3f39773edfcbdf0"
}


@criterion(description="The reviewed source is unchanged")
def source_preserved(workspace: Path):
    return all((workspace / name).is_file() and hashlib.sha256((workspace / name).read_bytes()).hexdigest() == digest for name, digest in HASHES.items())
