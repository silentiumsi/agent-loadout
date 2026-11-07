FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app/project
COPY slug.py test_slug.py ./
COPY setup.sh /tmp/setup.sh
RUN sh /tmp/setup.sh
COPY git /usr/local/bin/git
RUN chmod +x /usr/local/bin/git && touch /app/worktree-additions.jsonl
