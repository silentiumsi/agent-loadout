FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN git init -b main && git config user.name 'Eval User' && git config user.email eval@example.invalid && git commit --allow-empty -m 'chore: initial fixture'
