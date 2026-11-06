FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /uvx /usr/local/bin/
RUN uvx --python '>=3.12,<3.14' --from 'harbor-rewardkit==0.2.*' rewardkit --help > /dev/null
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && rm -rf /var/lib/apt/lists/* && curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="/root/.local/bin:$PATH"
COPY . /tests/
WORKDIR /app
