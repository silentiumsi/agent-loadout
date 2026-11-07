FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git jq ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app/project
RUN git init -b main && git config user.name 'Eval User' && git config user.email eval@example.invalid && git commit --allow-empty -m 'chore: initial fixture' && git remote add origin https://github.com/eval-fixture/widget.git
COPY gh /usr/local/bin/gh
RUN chmod +x /usr/local/bin/gh
