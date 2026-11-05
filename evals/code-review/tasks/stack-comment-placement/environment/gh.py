#!/usr/bin/env python3
"""Minimal offline stand-in for the GitHub CLI over a local stacked-PR fixture.

Reads PR metadata and diffs from the local repo. Records every comment or review
posted to GH_FAKE_LOG as JSON lines. Inline comments are rejected like GitHub
rejects them: the path and line must lie inside the diff of the target PR.
"""
import json
import os
import re
import subprocess
import sys

REPO = "acme/shop"
APP = os.environ.get("GH_FAKE_APP", "/app")
LOG = os.environ.get("GH_FAKE_LOG", "/logs/agent/gh-posts.jsonl")
PRS = json.load(open(os.environ.get("GH_FAKE_PRS", "/opt/gh/prs.json")))


def die(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def git(*args):
    return subprocess.run(["git", "-C", APP, *args], capture_output=True, text=True, check=True).stdout


def pr_by_number(number):
    for pr in PRS:
        if pr["number"] == int(number):
            return pr
    die(f"GraphQL: Could not resolve to a PullRequest with the number of {number}. (repository.pullRequest)")


def current_pr():
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    for pr in PRS:
        if pr["headRefName"] == branch:
            return pr
    die(f'could not find any pull requests for branch "{branch}"')


def diff_for(pr, path=None):
    args = ["diff", f"{pr['baseRefName']}..{pr['headRefName']}"]
    return git(*args, "--", path) if path else git(*args)


def changed_files(pr):
    return [f for f in git("diff", "--name-only", f"{pr['baseRefName']}..{pr['headRefName']}").split("\n") if f]


def diff_lines(pr, path):
    """Return {new_line: position} for lines visible in the PR diff of path."""
    visible, position, new_line, seen_header = {}, 0, 0, False
    for row in diff_for(pr, path).split("\n"):
        if row.startswith(("diff ", "index ", "--- ", "+++ ", "new file", "deleted file")):
            continue
        header = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", row)
        if header:
            new_line = int(header.group(1)) - 1
            position += 1 if seen_header else 0
            seen_header = True
            continue
        position += 1
        if row.startswith("-"):
            continue
        if row.startswith(("+", " ")):
            new_line += 1
            visible[new_line] = position
    return visible


def record(entry):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as handle:
        handle.write(json.dumps(entry) + "\n")


def post_inline(pr, body, path, line=None, position=None):
    if path not in changed_files(pr):
        unprocessable("path", f"{path} is not part of pull request #{pr['number']}")
    visible = diff_lines(pr, path)
    if line is None and position is not None:
        line = next((n for n, p in visible.items() if p == int(position)), None)
    if line is None or int(line) not in visible:
        unprocessable("line", "could not be resolved: the line is not part of the diff")
    record({"pr": pr["number"], "kind": "inline", "path": path, "line": int(line), "body": body})


def unprocessable(field, message):
    print(json.dumps({"message": "Validation Failed", "errors": [{"resource": "PullRequestReviewComment", "code": "custom", "field": field, "message": message}]}))
    die("gh: Validation Failed (HTTP 422)")


def read_body(options):
    if "body" in options:
        return options["body"]
    if "body-file" in options:
        path = options["body-file"]
        return sys.stdin.read() if path == "-" else open(path).read()
    die("body required")


def parse(argv, value_flags):
    """Split argv into positionals and {flag: value}; value_flags take an argument."""
    positional, options, repeated = [], {}, []
    short = {"b": "body", "F": "field", "f": "raw-field", "q": "jq", "X": "method", "t": "title", "R": "repo", "c": "comment"}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg.startswith("--") or (arg.startswith("-") and len(arg) == 2):
            name, _, inline = arg.lstrip("-").partition("=")
            name = short.get(name, name)
            if name in value_flags:
                value = inline if inline else argv[i + 1]
                i += 0 if inline else 1
                if name in ("field", "raw-field"):
                    repeated.append(value)
                else:
                    options[name] = value
            else:
                options[name] = True
        else:
            positional.append(arg)
        i += 1
    return positional, options, repeated


def emit(data, options):
    text = json.dumps(data)
    if "jq" in options:
        text = subprocess.run(["jq", "-r", options["jq"]], input=text, capture_output=True, text=True).stdout.rstrip("\n")
    print(text)


def pr_json(pr):
    files = [{"path": p, "additions": 0, "deletions": 0} for p in changed_files(pr)]
    return {**pr, "number": pr["number"], "state": "OPEN", "files": files, "comments": [], "reviews": [], "url": f"https://github.com/{REPO}/pull/{pr['number']}"}


def pr_command(argv):
    sub, rest = argv[0], argv[1:]
    positional, options, _ = parse(rest, {"json", "jq", "body", "body-file", "repo", "title", "base"})
    if sub == "list":
        return emit([pr_json(p) for p in PRS], options) if "json" in options else print("\n".join(f"#{p['number']}\t{p['title']}\t{p['headRefName']}" for p in PRS))
    pr = pr_by_number(positional[0]) if positional else current_pr()
    if sub == "view":
        if "json" in options:
            return emit({k: v for k, v in pr_json(pr).items() if k in options["json"].split(",")}, options)
        return print(f"title:\t{pr['title']}\nbase:\t{pr['baseRefName']}\nhead:\t{pr['headRefName']}\n--\n{pr['body']}")
    if sub == "diff":
        return print("\n".join(changed_files(pr))) if "name-only" in options else print(diff_for(pr), end="")
    if sub == "comment":
        return record({"pr": pr["number"], "kind": "pr-comment", "body": read_body(options)})
    if sub == "review":
        state = "APPROVE" if "approve" in options else "REQUEST_CHANGES" if "request-changes" in options else "COMMENT"
        return record({"pr": pr["number"], "kind": "review-body", "state": state, "body": read_body(options) if ("body" in options or "body-file" in options) else ""})
    if sub == "checkout":
        git("checkout", pr["headRefName"])
        return
    die(f"gh pr {sub}: unsupported in this fixture")


def api_command(argv):
    positional, options, fields = parse(argv, {"jq", "method", "field", "raw-field", "input", "header", "H"})
    endpoint = positional[0].lstrip("/").replace("{owner}", REPO.split("/")[0]).replace("{repo}", REPO.split("/")[1])
    payload = {}
    if "input" in options:
        payload = json.loads(sys.stdin.read() if options["input"] == "-" else open(options["input"]).read())
    for field in fields:
        key, _, value = field.partition("=")
        payload[key] = int(value) if key in ("line", "position") and value.isdigit() else value
    method = options.get("method", "POST" if payload else "GET").upper()
    match = re.fullmatch(rf"repos/{REPO}/(pulls|issues)(?:/(\d+))?(?:/(comments|reviews|files))?", endpoint)
    if not match:
        die(f"gh api: unsupported endpoint {endpoint}")
    kind, number, leaf = match.groups()
    if method == "GET":
        if not number:
            return emit([pr_json(p) for p in PRS], options)
        pr = pr_by_number(number)
        if leaf == "files":
            return emit([{"filename": f, "patch": diff_for(pr, f)} for f in changed_files(pr)], options)
        return emit(pr_json(pr) if not leaf else [], options)
    pr = pr_by_number(number)
    if kind == "issues" and leaf == "comments":
        record({"pr": pr["number"], "kind": "pr-comment", "body": payload.get("body", "")})
    elif kind == "pulls" and leaf == "comments":
        post_inline(pr, payload.get("body", ""), payload.get("path"), payload.get("line"), payload.get("position"))
    elif kind == "pulls" and leaf == "reviews":
        for comment in payload.get("comments", []):
            post_inline(pr, comment.get("body", ""), comment.get("path"), comment.get("line"), comment.get("position"))
        if payload.get("body"):
            record({"pr": pr["number"], "kind": "review-body", "state": payload.get("event", "COMMENT"), "body": payload["body"]})
    else:
        die(f"gh api: unsupported endpoint {endpoint}")
    print(json.dumps({"id": 1}))


def main(argv):
    if not argv:
        die("gh: missing command")
    command, rest = argv[0], argv[1:]
    if command == "pr":
        return pr_command(rest)
    if command == "api":
        return api_command(rest)
    if command == "repo":
        return emit({"nameWithOwner": REPO, "name": "shop", "owner": {"login": "acme"}}, parse(rest, {"json", "jq"})[1]) if "--json" in rest else print(REPO)
    if command == "auth":
        return print(f"github.com\n  ✓ Logged in to github.com account fixture")
    die(f"gh {command}: unsupported in this fixture")


main(sys.argv[1:])
