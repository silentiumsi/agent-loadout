FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends jq \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/Documents/Personal /root/Documents/Work /root/.config/obsidian \
    && printf '# Personal notes\n' > /root/Documents/Personal/Home.md \
    && printf '# Work notes\n' > /root/Documents/Work/Home.md \
    && printf '%s' '{"vaults":{"personal":{"path":"/root/Documents/Personal"},"work":{"path":"/root/Documents/Work"}}}' \
       > /root/.config/obsidian/obsidian.json

WORKDIR /app
