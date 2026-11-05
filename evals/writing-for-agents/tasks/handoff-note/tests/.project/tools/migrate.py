import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description="Local migration fixture. Run from project root. `status` prints each module's state.")
sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("status", help="Print module states")
run = sub.add_parser("run", help="Queue a module migration (does not change status here)")
run.add_argument("module")
args = parser.parse_args()
state = json.loads(Path("migrations/state.json").read_text())
if args.command == "status":
    print(json.dumps(state))
else:
    print(json.dumps({"module": args.module, "queued": True}))
