"""Review-only task: the reviewed source must be unchanged."""
import hashlib
from pathlib import Path
from rewardkit import criterion

HASHES = {
    "app.py": "2196440fdd351f8abcae11d4346c2ddbe8a126b63ab95a62d84c72845e4ce08c",
    "test_app.py": "5e31cead07d5a3888930031fdc2002b1df60fdbbc6c4d170ab60c5daba6e4a48"
}


@criterion(description="The reviewed source is unchanged")
def source_preserved(workspace: Path):
    return all((workspace / name).is_file() and hashlib.sha256((workspace / name).read_bytes()).hexdigest() == digest for name, digest in HASHES.items())
