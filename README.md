# BGM Library - 免版权背景音乐库技能

为视频/音频项目添加高质量免版权背景音乐，支持自动混音、音量控制、淡入淡出。

## 功能特点

- **25首精选BGM**：涵盖5种风格，满足不同场景需求
- **自动混音**：智能添加背景音乐，保持原音频质量
- **淡入淡出**：专业的音频过渡效果
- **免版权**：所有BGM来自Fesliyan Studios，可商用无需署名
- **易于使用**：简单的命令行接口，快速上手

## 风格分类

| 风格 | 情绪 | 适用场景 | 曲目数 |
|------|------|---------|-------|
| `tech-corporate` | `ambient` | AI工具介绍、科技产品发布会 | 5 |
| `tech-corporate` | `upbeat` | 产品上线庆祝、功能更新 | 5 |
| `social-media` | `ambient` | Vlog、生活分享、旅行记录 | 5 |
| `social-media` | `upbeat` | 挑战视频、好物推荐、趣味实验 | 5 |
| `startup` | `upbeat` | 创业故事、团队介绍、愿景展望 | 5 |

## 安装方法

### 方法1：从 .skill 文件安装

1. 下载 `bgm-library.skill` 文件
2. 运行安装命令：
   ```bash
   openclaw skill install bgm-library.skill
   ```

### 方法2：从源代码安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/qianqiuwanzi/bgm-library.git
   ```
2. 复制到技能目录：
   ```bash
   cp -r bgm-library ~/.qclaw/skills/
   ```

## 使用方法

### 自动添加 BGM（推荐）

使用 `scripts/add_bgm.py` 脚本自动混音：

```bash
python scripts/add_bgm.py \
  --input <输入视频.mp4> \
  --output <输出视频.mp4> \
  --style <风格> \
  --mood <情绪>
```

**参数说明**：
- `--input`: 输入视频路径（必需）
- `--output`: 输出视频路径（必需）
- `--style`: 风格类别（可选，默认 `tech-corporate`）
  - `tech-corporate`: 科技/商务
  - `social-media`: 自媒体/生活
  - `startup`: 创业/梦想
- `--mood`: 情绪类型（可选，默认 `ambient`）
  - `ambient`: 环境感（沉稳、背景）
  - `upbeat`: 活力感（轻快、激励）
- `--volume`: BGM 音量（可选，默认 `0.15`，范围 0.0-1.0）
- `--fade-in`: 淡入时长秒数（可选，默认 `2.0`）
- `--fade-out`: 淡出时长秒数（可选，默认 `3.0`）

**示例**：
```bash
# 科技商务风格，环境感
python scripts/add_bgm.py --input video.mp4 --output video_bgm.mp4 --style tech-corporate --mood ambient

# 自媒体生活风格，活力感
python scripts/add_bgm.py --input vlog.mp4 --output vlog_bgm.mp4 --style social-media --mood upbeat
```

### 手动混音（FFmpeg 命令）

如果需要更精细控制，可直接用 FFmpeg：

```bash
ffmpeg -y \
  -i <输入视频.mp4> \
  -i <BGM文件.mp3> \
  -filter_complex "[1:a]volume=0.15,afade=type=in:st=0:d=2,afade=type=out:st=<视频时长-3>:d=3[BGM];[0:a][BGM]amix=inputs=2:duration=first:normalize=0[mixed]" \
  -map 0:v -map [mixed] \
  -c:v copy -c:a aac -b:a 192k \
  <输出视频.mp4>
```

## 添加新 BGM

### 1. 下载新曲目

从以下平台下载免版权 BGM：
- **Fesliyan Studios**: https://www.fesliyanstudios.com/
- **Pixabay Music**: https://pixabay.com/music/
- **YouTube Audio Library**: https://www.youtube.com/audiolibrary

### 2. 放入对应目录

将下载的 MP3 文件放入 `assets/music-library/<风格>/<情绪>/` 目录。

### 3. 更新清单

运行 `scripts/gen_bgm.py` 更新 `assets/bgm_manifest.json`：

```bash
python scripts/gen_bgm.py --scan assets/music-library --output assets/bgm_manifest.json
```

## 依赖要求

- Python 3.6+
- FFmpeg（需在 PATH 中）

## 注意事项

1. **BGM 音量**：默认 0.15（15%），可根据需要调整。建议范围：0.10-0.20
2. **淡入淡出**：默认淡入 2s、淡出 3s。可根据视频节奏调整
3. **两段式混音**：先混合所有音轨，再添加 BGM。避免 TTS 音量被稀释
4. **素材版权**：仅使用 `assets/music-library/` 中的素材，或确保下载的素材是免版权的

## 故障排除

### BGM 未添加

- 检查 `assets/music-library/` 目录是否存在
- 检查 `assets/bgm_manifest.json` 是否存在
- 运行 `python scripts/gen_bgm.py` 重新生成清单

### 混音后无音频

- 检查输入视频是否有音频轨道（`ffprobe <视频.mp4>`）
- 检查 BGM 文件是否有效（`ffprobe <bgm.mp3>`）

### 音量不平衡

- 调整 `--volume` 参数（降低 BGM 音量，或提升 TTS 音量）
- 使用 FFmpeg 手动调整（`volume` 滤镜）

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 支持

如果您遇到任何问题或有建议，请打开一个 issue。