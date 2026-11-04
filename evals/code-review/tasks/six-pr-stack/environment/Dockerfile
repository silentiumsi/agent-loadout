FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY base/ /app/
RUN git init -b main && git config user.name Fixture && git config user.email fixture@example.test && git add . && git commit -m Base && git tag base
COPY changes/ /changes/
RUN set -eu; for change in /changes/*; do cp -a "$change/." /app/; git add .; git add --renormalize .; git commit --allow-empty -m "Change ${change##*/}"; git tag "pr-${change##*/}"; done && git diff --exit-code HEAD && test "$(git rev-list --count base..HEAD)" -eq 6
