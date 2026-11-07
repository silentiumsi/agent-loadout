FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN uv pip install --system 'harbor-rewardkit==0.2.3'
WORKDIR /app
COPY . /tests/
