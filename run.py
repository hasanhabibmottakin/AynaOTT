import os
import re
import json
import requests
from datetime import datetime

API_FILE = "api.json"
PLAYLIST_FILE = "playlist.m3u"
OUTPUT_FILE = "rest_api.json"

BASE_URL = os.getenv("AYNA_BASE_URL")  

def fetch_html(url: str) -> str:
    """Fetch HTML safely. Return empty string if fails."""
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if res.status_code == 200:
            return res.text
    except Exception:
        pass
    return ""  

def extract_stream_url(html: str) -> str:
    """Extract m3u8 URL from HTML using regex."""
    match = re.search(r'const\s+streamUrl\s*=\s*"([^"]+)"', html)
    return match.group(1) if match else ""

def main():
    if not BASE_URL:
        print("Missing AYNA_BASE_URL environment variable.")
        return

    
    try:
        with open(API_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        print(" Failed to read api.json")
        return

    channels = data.get("channels", [])
    result = {"updated": datetime.utcnow().isoformat(), "channels": []}
    m3u_lines = ["#EXTM3U"]

    for ch in channels:
        cid = ch.get("id")
        title = ch.get("title", "Unknown")
        logo = ch.get("logo", "")
        cat = ch.get("category", "Others")

        print(f" Fetching: {title}")

        html = fetch_html(f"{BASE_URL}{cid}")
        stream_url = extract_stream_url(html)

        if stream_url:
            ch["url"] = stream_url
            result["channels"].append(ch)
            m3u_lines.append(
                f'#EXTINF:-1 tvg-id="{cid}" tvg-name="{title}" '
                f'tvg-logo="{logo}" group-title="{cat}",{title}\n{stream_url}'
            )
        else:
            print(f"Skipped: {title} (no valid URL)")

    
    with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("playlist.m3u & rest_api.json generated successfully!")

if __name__ == "__main__":
    main()
