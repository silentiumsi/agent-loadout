FROM node:22.16.0-bookworm-slim AS compiler
RUN npm install --prefix /opt typescript@5.9.3
FROM python:3.12-slim
COPY --from=compiler /usr/local/bin/node /usr/local/bin/node
COPY --from=compiler /opt/node_modules /opt/node_modules
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/
RUN uv pip install --system 'harbor-rewardkit==0.2.3'
ENV NODE_PATH=/opt/node_modules
ENV LITELLM_LOCAL_MODEL_COST_MAP=True
COPY . /tests/
WORKDIR /app
