FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ripgrep && rm -rf /var/lib/apt/lists/*
COPY project /app/project
WORKDIR /app/project
RUN git init -q && git add . && git -c user.name=Fixture -c user.email=fixture@example.invalid commit -qm 'Initial exporter'
