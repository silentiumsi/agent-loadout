import argparse
import sys

parser = argparse.ArgumentParser(description="Kestrel deploy CLI (local fixture). Names over 40 characters are rejected.")
sub = parser.add_subparsers(dest="command", required=True)
deploy = sub.add_parser("deploy", help="Deploy a service")
deploy.add_argument("name")
deploy.add_argument("--region", choices=("eu-west", "us-east"), required=True)
args = parser.parse_args()
if len(args.name) > 40:
    print("error: service name longer than 40 characters", file=sys.stderr)
    sys.exit(2)
print(f"deployed {args.name} to {args.region}")
