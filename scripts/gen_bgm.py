#!/usr/bin/env python3
"""
BGM 管理器 - 扫描 music-library 目录，生成 bgm_manifest.json
用法:
    python gen_bgm.py --scan "D:/workspace/music-library" --output "D:/workspace/music-library/bgm_manifest.json"
    python gen_bgm.py --preview "D:/workspace/music-library/xxx.mp3" --tts "D:/workspace/xxx/assets/tts_mixed.aac"
"""

import os
import json
import subprocess
import argparse
import sys

# ── 配置 ────────────────────────────────────────────────────────────────────────

FFPROBE = r'D:\softwarefmpeg-8.1.1-full_buildinfprobe.exe'

# 自动查找 ffprobe
try:
    import shutil
    if not os.path.exists(FFPROBE):
        _fp = shutil.which('ffprobe')
        if _fp:
            FFPROBE = _fp
except Exception:
    pass

# ── 工具函数 ────────────────────────────────────────────────────────────────────

def get_mp3_info(filepath):
    """用 ffprobe 获取 mp3 的 duration/bpm 信息"""
    try:
        result = subprocess.run([
            FFPROBE, '-v', 'quiet',
            '-show_entries', 'format=duration',
            '-of', 'csv=p=0',
            filepath
        ], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            return {'duration': int(duration)}
    except Exception:
        pass
    return {'duration': 0}

def scan_music_library(library_root):
    """扫描 music-library 目录，生成清单"""
    manifest = {
        'version': '2026-06-07',
        'categories': {},
        'default': 'tech-corporate/ambient'
    }

    # 遍历二级目录（如 tech-corporate/ambient/）
    for category in os.listdir(library_root):
        category_path = os.path.join(library_root, category)
        if not os.path.isdir(category_path):
            continue

        manifest['categories'][category] = {}

        for mood in os.listdir(category_path):
            mood_path = os.path.join(category_path, mood)
            if not os.path.isdir(mood_path):
                continue

            tracks = []
            for filename in os.listdir(mood_path):
                if not filename.lower().endswith(('.mp3', '.wav', '.aac')):
                    continue

                filepath = os.path.join(mood_path, filename)
                info = get_mp3_info(filepath)

                tracks.append({
                    'file': filename,
                    'duration': info['duration'],
                    'volume': 0.15  # 默认音量
                })

            manifest['categories'][category][mood] = tracks

    return manifest

# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='BGM 管理器')
    parser.add_argument('--scan', help='扫描 music-library 目录')
    parser.add_argument('--output', help='输出 bgm_manifest.json 路径')
    parser.add_argument('--preview', help='预览混音效果（测试用）')
    parser.add_argument('--tts', help='TTS 音频路径（用于预览）')

    args = parser.parse_args()

    if args.scan and args.output:
        print(f'扫描: {args.scan}')
        manifest = scan_music_library(args.scan)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print(f'[OK] 清单已生成: {args.output}')
        print(f'    分类数: {len(manifest["categories"])}')
        total_tracks = sum(
            len(tracks)
            for cat in manifest['categories'].values()
            for tracks in cat.values()
        )
        print(f'   总曲目数: {total_tracks}')

    elif args.preview and args.tts:
        print('预览功能待实现（需 FFmpeg 混音测试）')
        sys.exit(0)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()