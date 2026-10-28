
import json
from pathlib import Path

source = Path("Channels.json")
output = Path("playlist.m3u")

data = json.loads(source.read_text(encoding="utf-8"))
channels = data.get("channels", [])
lines = ["#EXTM3U"]

for channel in channels:
    if channel.get("enabled") is not True:
        continue

    url = (channel.get("streamUrl") or "").strip()
    if not url:
        continue

    def clean(value):
        return str(value or "").replace('"', "'").strip()

    name = clean(channel.get("name")) or "Channel"
    logo = clean(channel.get("logo"))
    category = clean(channel.get("category")) or "Lainnya"
    channel_id = clean(channel.get("id"))

    metadata = (
        f'#EXTINF:-1 tvg-id="{channel_id}" '
        f'tvg-name="{name}" tvg-logo="{logo}" '
        f'group-title="{category}",{name}'
    )

    lines.extend([metadata, url])

output.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Playlist dibuat: {len(lines) // 2} baris termasuk header.")
