"""Review-only task: the reviewed source must be unchanged."""
import hashlib
from pathlib import Path
from rewardkit import criterion

HASHES = {
    "pager.py": "9c910c92ff64eca381b8a715fb824f96ce391a7df4112e5d90b8dfbe91f2b331",
    "test_pager.py": "418e66f84f56076df2aedadd78c594ec8436e410671ada68a6c26ddc371b8da3"
}


@criterion(description="The reviewed source is unchanged")
def source_preserved(workspace: Path):
    return all((workspace / name).is_file() and hashlib.sha256((workspace / name).read_bytes()).hexdigest() == digest for name, digest in HASHES.items())
