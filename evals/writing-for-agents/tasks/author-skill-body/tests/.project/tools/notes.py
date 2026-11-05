import argparse
import json

parser = argparse.ArgumentParser(description="Draft release notes from commits (local fixture). Exits 0 even with warnings; inspect them.")
sub = parser.add_subparsers(dest="command", required=True)
draft = sub.add_parser("draft", help="Print JSON {entries, warnings} for commits since a tag")
draft.add_argument("--since", required=True)
parser.parse_args()
print(json.dumps({"entries": [], "warnings": ["commit 3fa91c has no impact tag"]}))
