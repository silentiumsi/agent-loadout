FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates jq && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY base/ /app/
RUN git init -b main && git config user.name Fixture && git config user.email fixture@example.test && git add . && git commit -m Base && git tag base
COPY changes/ /changes/
RUN for n in 1 2 3; do git checkout -q -b "stack-$n"; cp -a "/changes/$n/." /app/; git add .; git commit -m "Change $n"; git tag "pr-$n"; done
COPY prs.json /opt/gh/prs.json
COPY gh.py /usr/local/bin/gh
RUN chmod +x /usr/local/bin/gh && mkdir -p /logs/agent
