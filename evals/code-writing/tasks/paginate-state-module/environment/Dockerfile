FROM node:22.16.0-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ripgrep python3 && rm -rf /var/lib/apt/lists/*
COPY project /app/project
WORKDIR /app/project
