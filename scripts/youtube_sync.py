
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCxvhyYARWKIg0HRX5z10_hQ"
FEED_URL = (
    "https://www.youtube.com/feeds/videos.xml"
    f"?channel_id={CHANNEL_ID}"
)

SUPABASE_URL = os.environ["https://aewbseqmlriyoeugvchm.supabase.co"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
TABLE_URL = f"{SUPABASE_URL}/rest/v1/content"

ATOM = "{http://www.w3.org/2005/Atom}"
YT = "{http://www.youtube.com/xml/schemas/2015}"
MEDIA = "{http://search.yahoo.com/mrss/}"



def request(url, method="GET", data=None, prefer=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    if prefer:
        headers["Prefer"] = prefer

    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            status = response.status
            content_type = response.headers.get("Content-Type", "")

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase HTTP error {error.code}: {details[:500]}"
        ) from error

    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        preview = raw[:300].decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Expected JSON from Supabase; HTTP {status}; "
            f"Content-Type: {content_type}; Response: {preview}"
        ) from error


def main():
    feed_req = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "ZUBAiR-Tech-Talks-Sync/1.0"},
    )

    with urllib.request.urlopen(feed_req, timeout=30) as response:
        feed_xml = response.read()

    root = ET.fromstring(feed_xml)
    entries = root.findall(f"{ATOM}entry")

    added = 0
    skipped = 0

    for entry in entries:
        video_id = entry.findtext(f"{YT}videoId")
        title = entry.findtext(f"{ATOM}title")

        if not video_id or not title:
            skipped += 1
            continue

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        title = title.strip()

        media_group = entry.find(f"{MEDIA}group")
        description = ""
        thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

        if media_group is not None:
            description = (
                media_group.findtext(f"{MEDIA}description") or ""
            ).strip()

            thumb = media_group.find(f"{MEDIA}thumbnail")
            if thumb is not None and thumb.get("url"):
                thumbnail = thumb.get("url")

        query = urllib.parse.urlencode({
            "select": "id",
            "external_url": f"eq.{video_url}",
            "limit": "1",
        })

        existing = request(f"{TABLE_URL}?{query}")

        if existing:
            print(f"Already exists: {title}")
            skipped += 1
            continue

        record = {
            "title": title,
            "slug": f"youtube-{video_id}",
            "content_type": "video",
            "description": description,
            "image_url": thumbnail,
            "external_url": video_url,
            "status": "draft",
        }

        request(
            TABLE_URL,
            method="POST",
            data=record,
            prefer="return=minimal",
        )

        print(f"Added draft: {title}")
        added += 1

    print(f"Sync complete. Added: {added}; skipped: {skipped}")


if __name__ == "__main__":
    main()
