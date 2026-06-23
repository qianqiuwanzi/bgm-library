#!/usr/bin/env python3
"""从 Mixkit 批量下载 BGM（带标题匹配）"""
import os, requests, re, json, time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BASE_DIR = r"D:\OpenClaw\workspace\skills\bgm-library\assets\music-library"

def parse_mixkit_page(tag):
    """Parse Mixkit page, return list of (url, title)"""
    url = f"https://mixkit.co/free-stock-music/{tag}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return []
        text = r.text
        tracks = []
        # Extract NUXT JSON data
        nuxt_match = re.search(r'window\.__NUXT__\s*=\s*(\{.+)', text)
        if nuxt_match:
            try:
                nuxt_data = json.loads(nuxt_match.group(1))
                def find_tracks(obj, depth=0):
                    result = []
                    if depth > 10:
                        return result
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, list) and len(v) > 0:
                                for item in v:
                                    if isinstance(item, dict):
                                        audio = item.get("audio") or item.get("audioUrl") or item.get("url")
                                        title = item.get("title") or item.get("name") or item.get("slug")
                                        if audio and isinstance(audio, str) and ".mp3" in audio:
                                            result.append((audio, title or ""))
                            result.extend(find_tracks(v, depth+1))
                    elif isinstance(obj, list):
                        for item in obj:
                            result.extend(find_tracks(item, depth+1))
                    return result
                tracks = find_tracks(nuxt_data)
            except (json.JSONDecodeError, Exception):
                pass
        # Fallback: extract MP3 URLs from HTML
        if not tracks:
            mp3_urls = re.findall(r'(https://assets\.mixkit\.co/music/\d+/\d+\.mp3)', text)
            for mp3_url in mp3_urls[:10]:
                tracks.append((mp3_url, ""))
        return tracks
    except Exception as e:
        print(f"  Error: {e}")
    return []

def dl_file(url, path):
    """Download file"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return os.path.getsize(path) > 5000
    except:
        pass
    return False

def probe_duration(path):
    """Get audio duration with ffprobe"""
    import subprocess
    cmd = ['D:/software/ffmpeg-8.1.1-full_build/bin/ffprobe.exe',
           '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'default=noprint_wrappers=1:nokey=1', path]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(r.stdout.strip() or 0)
    except:
        return 0

# Mixkit tag -> filename slug -> style/mood
TAG_MAP = [
    ("cinematic",   "void.mp3",             "tech-corporate", "ambient"),
    ("corporate",   "intro.mp3",             "tech-corporate", "upbeat"),
    ("piano",       "melody.mp3",            "tech-corporate", "ambient"),
    ("happy",       "sunrise.mp3",           "social-media",   "ambient"),
    ("urban",       "busy_life.mp3",         "social-media",   "upbeat"),
    ("cinematic",   "faded.mp3",              "social-media",   "ambient"),
    ("ambient",    "fresh_girl.mp3",         "social-media",   "ambient"),
    ("piano",      "a_little_story.mp3",     "social-media",   "ambient"),
    ("electronic", "huandezhou.mp3",          "startup",        "upbeat"),
    ("dramatic",   "comedian_king.mp3",       "tech-corporate", "ambient"),
    ("dramatic",   "you_dont_know_me.mp3",    "tech-corporate", "upbeat"),
    ("happy",      "oops.mp3",               "social-media",   "upbeat"),
    ("cinematic",  "despair.mp3",            "tech-corporate", "ambient"),
    ("inspiring",  "nothing_to_fear.mp3",    "startup",        "upbeat"),
    ("piano",      "feeling.mp3",           "social-media",   "ambient"),
    ("ambient",    "firefly.mp3",            "social-media",   "ambient"),
    ("action",     "i_win_u_lose.mp3",       "startup",        "upbeat"),
    ("chill",      "after_hours.mp3",        "social-media",   "ambient"),
    ("love",       "beside_you.mp3",         "social-media",   "ambient"),
    ("jazz",       "groove.mp3",             "social-media",   "upbeat"),
    ("action",     "catching.mp3",           "startup",        "upbeat"),
]

downloaded = []
failed = []

for i, (tag, fname, style, mood) in enumerate(TAG_MAP):
    msg = f"[{i+1}/{len(TAG_MAP)}] {fname} (tag={tag})"
    print(msg, flush=True)

    tracks = parse_mixkit_page(tag)
    if not tracks:
        print(f"  NO tracks for tag '{tag}'")
        failed.append((fname, tag, "no tracks"))
        continue

    mp3_url, title = tracks[0]
    label = title or "untitled"
    print(f"  -> {label}: {mp3_url}")

    dest_dir = os.path.join(BASE_DIR, style, mood)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, fname)

    ok = dl_file(mp3_url, dest)
    if ok:
        sz = os.path.getsize(dest)
        dur = probe_duration(dest)
        print(f"  OK {sz//1024}KB, {dur:.0f}s -> {style}/{mood}/{fname}")
        downloaded.append((fname, label, sz, dur))
    else:
        print(f"  FAIL download")
        failed.append((fname, tag, mp3_url))
    time.sleep(0.3)

print(f"\n{'='*60}")
print(f"Done: {len(downloaded)}/{len(TAG_MAP)} downloaded")
if downloaded:
    print("\nDownloaded:")
    for fname, title, sz, dur in downloaded:
        print(f"  {fname} | {title} | {sz//1024}KB | {dur:.0f}s")
if failed:
    print(f"\nFailed ({len(failed)}):")
    for fn, tag, info in failed:
        print(f"  {fn} (tag={tag}): {info}")
