FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/

RUN uv pip install --system 'harbor-rewardkit==0.2.3'
ENV LITELLM_LOCAL_MODEL_COST_MAP=True

WORKDIR /app

COPY . /tests/
