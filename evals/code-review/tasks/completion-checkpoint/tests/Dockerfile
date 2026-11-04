FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/
RUN apt-get update && apt-get install -y --no-install-recommends bash curl ca-certificates git ripgrep && rm -rf /var/lib/apt/lists/*
RUN uv pip install --system 'harbor-rewardkit==0.2.3'
RUN curl -fsSL https://chatgpt.com/codex/install.sh -o /tmp/install-codex.sh && CODEX_NON_INTERACTIVE=1 CODEX_RELEASE=0.166.0 CODEX_INSTALL_DIR=/usr/local/bin sh /tmp/install-codex.sh && rm /tmp/install-codex.sh
ENV LITELLM_LOCAL_MODEL_COST_MAP=True
WORKDIR /app
COPY . /tests/
