FROM ubuntu:24.04

# jq reads obsidian.json for vault discovery.
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq \
    && rm -rf /var/lib/apt/lists/*

COPY vault/ /root/Documents/Notes/

# The second vault is a stale entry whose folder no longer exists, as in a real obsidian.json.
RUN mkdir -p /root/.config/obsidian \
    && printf '%s' '{"vaults":{"3f9c1a2b7d4e8f01":{"path":"/root/Documents/Notes","ts":1761400000000,"open":true},"a1b2c3d4e5f60718":{"path":"/root/Old Vault","ts":1700000000000}}}' \
       > /root/.config/obsidian/obsidian.json

WORKDIR /app
