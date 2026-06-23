#!/usr/bin/env python3
"""从 Mixkit 下载免费 BGM"""
import os, requests, re, subprocess

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BASE_DIR = r"D:\OpenClaw\workspace\skills\bgm-library\assets\music-library"

def get_mixkit_tracks(tag):
    """获取 Mixkit 指定标签的音乐列表"""
    url = f"https://mixkit.co/free-stock-music/{tag}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return []
        text = r.text
        # 找音频URL
        pattern = r'https://assets\.mixkit\.co/music/preview/mixkit-[a-z0-9_-]+\.mp3'
        urls = re.findall(pattern, text)
        # 找标题
        titles = re.findall(r'"name"\s*:\s*"([^"]+)"', text)
        return list(zip(urls[:5], titles[:5]))
    except Exception as e:
        print(f"Error: {e}")
    return []

def dl_file(url, path):
    """下载文件"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return os.path.exists(path)
    except:
        pass
    return False

# Mixkit 标签 → 风格映射
TAG_MAP = [
    # (mixkit_tag, slug, style, mood)
    ("ambient", "void", "tech-corporate", "ambient"),
    ("corporate", "intro", "tech-corporate", "upbeat"),
    ("piano", "melody", "tech-corporate", "ambient"),
    ("happy", "sunrise", "social-media", "ambient"),
    ("urban", "busy_life", "social-media", "upbeat"),
    ("cinematic", "faded", "social-media", "ambient"),
    ("romantic", "fresh_girl", "social-media", "ambient"),
    ("love", "a_little_story", "social-media", "ambient"),
    ("electronic", "huandezhou", "startup", "upbeat"),
    ("dramatic", "comedian_king", "tech-corporate", "ambient"),
    ("sad", "you_dont_know_me", "tech-corporate", "upbeat"),
    ("fun", "oops", "social-media", "upbeat"),
    ("dark", "despair", "tech-corporate", "ambient"),
    ("inspiring", "nothing_to_fear", "startup", "upbeat"),
    ("beautiful", "feeling", "social-media", "ambient"),
    ("nature", "firefly", "social-media", "ambient"),
    ("action", "i_win_u_lose", "startup", "upbeat"),
    ("chill", "after_hours", "social-media", "ambient"),
    ("ballad", "beside_you", "social-media", "ambient"),
    ("jazz", "groove", "social-media", "upbeat"),
    ("drums", "catching", "startup", "upbeat"),
]

downloaded = []
failed = []

for tag, slug, style, mood in TAG_MAP:
    print(f"\nTag: {tag} -> {slug}.mp3")
    tracks = get_mixkit_tracks(tag)
    if not tracks:
        print(f"  No tracks found for tag '{tag}'")
        failed.append(slug)
        continue

    url, title = tracks[0]
    print(f"  Found: {title}")
    print(f"  URL: {url[:80]}...")

    dest_dir = os.path.join(BASE_DIR, style, mood)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"{slug}.mp3")

    if dl_file(url, dest):
        sz = os.path.getsize(dest)
        print(f"  OK: {sz//1024}KB -> {style}/{mood}/{slug}.mp3")
        downloaded.append(slug)
    else:
        print(f"  FAILED to download")
        failed.append(slug)

print(f"\n{'='*50}")
print(f"Downloaded: {len(downloaded)}/{len(TAG_MAP)}")
if failed:
    print(f"Failed: {failed}")
