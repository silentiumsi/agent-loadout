FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/

RUN uv pip install --system 'harbor-rewardkit==0.2.3' 'PyYAML==6.0.3'
# Reward Kit imports LiteLLM; use its bundled cost map without a network fetch.
ENV LITELLM_LOCAL_MODEL_COST_MAP=True

WORKDIR /app

COPY . /tests/
