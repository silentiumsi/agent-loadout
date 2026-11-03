#!/bin/sh
# Print the path of each Obsidian vault, one per line.

case "$(uname -s)" in
  Darwin) config="$HOME/Library/Application Support/obsidian/obsidian.json" ;;
  Linux) config="${XDG_CONFIG_HOME:-$HOME/.config}/obsidian/obsidian.json" ;;
  *) echo "Unsupported OS" >&2; exit 1 ;;
esac

command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }
[ -r "$config" ] || { echo "Obsidian config not found or unreadable: $config" >&2; exit 1; }

vaults="$(jq -r '.vaults[]?.path | select(type == "string" and length > 0)' "$config")" || { echo "Obsidian config is not valid JSON: $config" >&2; exit 1; }

if [ -z "$vaults" ]; then
  echo "No vaults found" >&2
  exit 1
fi

found=1
while IFS= read -r path; do
  [ -d "$path" ] && echo "$path" && found=0
done <<EOT
$vaults
EOT

[ "$found" -eq 0 ] || { echo "No vault folder exists on disk" >&2; exit 1; }
