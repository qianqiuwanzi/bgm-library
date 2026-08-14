# BGM Library - Royalty-Free Background Music Skill

> [English](README.md) · [中文](README_zh.md)

Add high-quality royalty-free background music to your video / audio projects, with auto mixing, volume control, and fade in / out.

## Features

- **25 curated BGM tracks**: 5 styles covering different scenarios
- **Auto mixing**: smartly add background music while preserving original audio quality
- **Fade in / out**: professional audio transitions
- **Royalty-free**: all BGM from Fesliyan Studios, free for commercial use, no attribution required
- **Easy to use**: simple CLI, quick to get started

## Style Categories

| Style | Mood | Use case | Tracks |
|------|------|---------|-------|
| `tech-corporate` | `ambient` | AI tool intros, tech product launches | 5 |
| `tech-corporate` | `upbeat` | Product launch celebration, feature updates | 5 |
| `social-media` | `ambient` | Vlogs, life sharing, travel logs | 5 |
| `social-media` | `upbeat` | Challenge videos, product recs, fun experiments | 5 |
| `startup` | `upbeat` | Startup stories, team intros, vision | 5 |

## Installation

### Method 1: Install from .skill file

1. Download the `bgm-library.skill` file
2. Run the install command:
   ```bash
   openclaw skill install bgm-library.skill
   ```

### Method 2: Install from source

1. Clone the repo:
   ```bash
   git clone https://github.com/qianqiuwanzi/bgm-library.git
   ```
2. Copy to the skills directory:
   ```bash
   cp -r bgm-library ~/.qclaw/skills/
   ```

## Usage

### Auto add BGM (recommended)

Use `scripts/add_bgm.py` for auto mixing:

```bash
python scripts/add_bgm.py \
  --input <input_video.mp4> \
  --output <output_video.mp4> \
  --style <style> \
  --mood <mood>
```

**Parameters**:
- `--input`: input video path (required)
- `--output`: output video path (required)
- `--style`: style category (optional, default `tech-corporate`)
  - `tech-corporate`: tech / business
  - `social-media`: social / life
  - `startup`: startup / dream
- `--mood`: mood type (optional, default `ambient`)
  - `ambient`: ambient (calm, background)
  - `upbeat`: energetic (lively, motivating)
- `--volume`: BGM volume (optional, default `0.15`, range 0.0-1.0)
- `--fade-in`: fade-in seconds (optional, default `2.0`)
- `--fade-out`: fade-out seconds (optional, default `3.0`)

**Examples**:
```bash
# Tech & business, ambient
python scripts/add_bgm.py --input video.mp4 --output video_bgm.mp4 --style tech-corporate --mood ambient

# Social & life, upbeat
python scripts/add_bgm.py --input vlog.mp4 --output vlog_bgm.mp4 --style social-media --mood upbeat
```

### Manual mixing (FFmpeg)

For finer control, use FFmpeg directly:

```bash
ffmpeg -y \
  -i <input_video.mp4> \
  -i <BGM_file.mp3> \
  -filter_complex "[1:a]volume=0.15,afade=type=in:st=0:d=2,afade=type=out:st=<video_duration-3>:d=3[BGM];[0:a][BGM]amix=inputs=2:duration=first:normalize=0[mixed]" \
  -map 0:v -map [mixed] \
  -c:v copy -c:a aac -b:a 192k \
  <output_video.mp4>
```

## Add New BGM

### 1. Download new tracks

Download royalty-free BGM from:
- **Fesliyan Studios**: https://www.fesliyanstudios.com/
- **Pixabay Music**: https://pixabay.com/music/
- **YouTube Audio Library**: https://www.youtube.com/audiolibrary

### 2. Place in the right directory

Put the downloaded MP3 into `assets/music-library/<style>/<mood>/`.

### 3. Update the manifest

Run `scripts/gen_bgm.py` to update `assets/bgm_manifest.json`:

```bash
python scripts/gen_bgm.py --scan assets/music-library --output assets/bgm_manifest.json
```

## Dependencies

- Python 3.6+
- FFmpeg (must be in PATH)

## Notes

1. **BGM volume**: default 0.15 (15%), adjustable. Suggested range: 0.10-0.20
2. **Fade in / out**: default fade-in 2s, fade-out 3s. Adjust to video rhythm
3. **Two-stage mixing**: mix all tracks first, then add BGM, to avoid diluting TTS volume
4. **Asset license**: only use assets in `assets/music-library/`, or ensure downloaded assets are royalty-free

## Troubleshooting

### BGM not added

- Check `assets/music-library/` exists
- Check `assets/bgm_manifest.json` exists
- Run `python scripts/gen_bgm.py` to regenerate the manifest

### No audio after mixing

- Check the input video has an audio track (`ffprobe <video.mp4>`)
- Check the BGM file is valid (`ffprobe <bgm.mp3>`)

### Volume imbalance

- Adjust `--volume` (lower BGM, or raise TTS volume)
- Use FFmpeg manually (`volume` filter)

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Feel free to open a Pull Request.

## Support

If you have any issues or suggestions, please open an issue.
