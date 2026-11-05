"""Review-only task: the reviewed source must be unchanged."""
import hashlib
from pathlib import Path
from rewardkit import criterion

HASHES = {
    "refunds.py": "ad2625930924d868a9ee4f11eca6611f80d70f4d005e77e0eb5488e70481f801",
    "test_refunds.py": "78bb9c726b48b52e8b8f0dac78234fce7b1f106fe1923693041a84a8a931c193",
    "docs/adr-007-refunds.md": "215e08428eee59f03bb1c0fc11d249cd283c4845b7eca96abb6aa30dadff5e23"
}


@criterion(description="The reviewed source is unchanged")
def source_preserved(workspace: Path):
    return all((workspace / name).is_file() and hashlib.sha256((workspace / name).read_bytes()).hexdigest() == digest for name, digest in HASHES.items())
