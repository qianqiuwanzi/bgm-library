#!/usr/bin/env python3
"""
为视频添加 BGM（自动混音 + 淡入淡出）
用法: python add_bgm.py --input <视频.mp4> --output <视频_bgm.mp4> --style <风格> --mood <情绪>
"""

import os
import sys
import json
import argparse
import subprocess
import random

# ── 配置 ────────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(SKILL_DIR, 'assets')
MUSIC_LIB = os.path.join(ASSETS_DIR, 'music-library')
MANIFEST_PATH = os.path.join(MUSIC_LIB, 'bgm_manifest.json')

# 自动查找 FFmpeg
FFMPEG = 'ffmpeg'
try:
    import shutil
    _ffmpeg = shutil.which('ffmpeg')
    if _ffmpeg:
        FFMPEG = _ffmpeg
except Exception:
    pass

# ── 核心功能 ───────────────────────────────────────────────────────────────────

def load_manifest():
    """加载 bgm_manifest.json"""
    if not os.path.exists(MANIFEST_PATH):
        print(f'[ERROR] Manifest 不存在: {MANIFEST_PATH}')
        print(f'请先运行: python gen_bgm.py --scan {MUSIC_LIB} --output {MANIFEST_PATH}')
        sys.exit(1)
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def select_bgm(manifest, style='tech-corporate', mood='ambient'):
    """从 manifest 中随机选择一首 BGM"""
    categories = manifest.get('categories', {})
    if style not in categories:
        print(f'[WARN] 风格不存在: {style}，使用默认: {manifest["default"]}')
        style, mood = manifest['default'].split('/')
    
    moods = categories[style]
    if mood not in moods:
        print(f'[WARN] 情绪不存在: {mood}，使用第一个可用的')
        mood = list(moods.keys())[0]
    
    tracks = moods[mood]
    if not tracks:
        print(f'[ERROR] 没有可用的 BGM: {style}/{mood}')
        sys.exit(1)
    
    pick = random.choice(tracks)
    bgm_path = os.path.join(MUSIC_LIB, style, mood, pick['file'])
    return bgm_path, pick

def add_bgm(input_video, output_video, bgm_path, volume=0.15, fade_in=2.0, fade_out=3.0):
    """为视频添加 BGM（两段式混音 + 淡入淡出）"""
    # 获取视频时长
    duration_cmd = [
        FFMPEG.replace('ffmpeg', 'ffprobe'),
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        input_video
    ]
    try:
        result = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=10)
        video_dur = float(result.stdout.strip())
        fade_out_start = max(0, video_dur - fade_out)
    except Exception:
        print('[WARN] 无法获取视频时长，淡出可能不准确')
        fade_out_start = 0
    
    # 两段式混音
    cmd = [
        FFMPEG, '-y',
        '-i', input_video,
        '-i', bgm_path,
        '-filter_complex',
        f'[1:a]volume={volume},afade=type=in:st=0:d={fade_in},'
        f'afade=type=out:st={fade_out_start}:d={fade_out}[BGM];'
        '[0:a][BGM]amix=inputs=2:duration=first:normalize=0[mixed]',
        '-map', '0:v', '-map', '[mixed]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        output_video
    ]
    
    print(f'[INFO] 添加 BGM: {os.path.basename(bgm_path)}')
    print(f'       音量: {volume}, 淡入: {fade_in}s, 淡出: {fade_out}s')
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f'[ERROR] FFmpeg 失败: {result.stderr[-500:]}')
        sys.exit(1)
    
    print(f'[OK] 输出: {output_video} ({os.path.getsize(output_video)/1024/1024:.1f}MB)')

# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='为视频添加 BGM')
    parser.add_argument('--input', required=True, help='输入视频路径')
    parser.add_argument('--output', required=True, help='输出视频路径')
    parser.add_argument('--style', default='tech-corporate', help='风格 (tech-corporate/social-media/startup)')
    parser.add_argument('--mood', default='ambient', help='情绪 (ambient/upbeat)')
    parser.add_argument('--volume', type=float, default=0.15, help='BGM 音量 (0.0-1.0)')
    parser.add_argument('--fade-in', type=float, default=2.0, help='淡入时长 (秒)')
    parser.add_argument('--fade-out', type=float, default=3.0, help='淡出时长 (秒)')
    parser.add_argument('--bgm', help='直接指定 BGM 文件路径（跳过随机选择）')
    
    args = parser.parse_args()
    
    # 检查输入
    if not os.path.exists(args.input):
        print(f'[ERROR] 输入视频不存在: {args.input}')
        sys.exit(1)
    
    # 选择 BGM
    if args.bgm and os.path.exists(args.bgm):
        bgm_path = args.bgm
        print(f'[INFO] 使用指定 BGM: {bgm_path}')
    else:
        manifest = load_manifest()
        bgm_path, pick = select_bgm(manifest, args.style, args.mood)
        print(f'[INFO] 随机选择 BGM: {pick["file"]} ({pick["duration"]}s)')
    
    # 添加 BGM
    add_bgm(args.input, args.output, bgm_path, args.volume, args.fade_in, args.fade_out)

if __name__ == '__main__':
    main()
