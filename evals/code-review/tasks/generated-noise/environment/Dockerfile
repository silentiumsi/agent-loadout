FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY base/ /app/
RUN git init -b main && git config user.name Fixture && git config user.email fixture@example.test && git add . && git commit -m Base && git tag base
COPY changes/ /changes/
COPY gen.py /gen/gen.py
RUN cp -a /changes/1/. /app/ && python3 /gen/gen.py /app && git add . && git commit -m "Change 1: regenerate types, refactor pagination" && git tag pr-1
