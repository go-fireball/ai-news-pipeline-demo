# AI News Pipeline Demo

An experimental pipeline that drafts an AI-generated news script with OpenAI, delivers narration through the text-to-speech API, and stitches everything into a short video using MoviePy. The goal is to keep the repo small and readable today so it can evolve later.

### 🎥 AI-Generated News Reader (Demo)

[Demo Video](./demo/result_voice.mp4)

## Project Layout
- `apps/ai-news/src/ai_news` contains modular code for configuration, script generation, TTS, and video assembly.
- `apps/ai-news/assets` stores the static background/avatar images used in the stitched video.
- `apps/ai-news/outputs` is auto-created at runtime with `scripts/`, `audio/`, and `video/` subfolders holding generated artifacts.
- `apps/ai-news/tests` is where pytest-based regression coverage belongs.

## Quick Start
1. `cd apps/ai-news && poetry install` to create the Python 3.12 virtual environment.
2. Define a `.env` file with `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_TTS_MODEL`, and `NEWS_DEFAULT_TOPIC` (defaults: `gpt-4.1-mini` and `gpt-4o-mini-tts`).
3. Run the pipeline end-to-end via `poetry run python -m ai_news.main --topic "AI Safety"`. If you omit `--topic`, the default topic is used.
4. Generated scripts, MP3 narration, and MP4 videos land in `apps/ai-news/outputs`; keep them out of version control.

## Development Notes
- Add tests under `apps/ai-news/tests` and run them with `poetry run pytest`.
- All configuration should flow through `config.get_settings()` so environment reads stay centralized.
- When debugging, you can execute only the script generator (`poetry run python -m ai_news.script_generator`) to avoid burning TTS/video credits.

## Future Lip-Sync Options
Simple static-image videos are fine for now, but you can add synced avatars when ready:
- **Wav2Lip**: Replace MoviePy composition with a pass that feeds narration audio and an avatar video loop through the pretrained Wav2Lip model. Requires PyTorch + GPU.
- **SadTalker or OpenTalker**: Run a local driving video pipeline to animate a portrait with lip sync; cache poses in `assets/` and generate mp4s in `outputs/video`.
- **Hosted APIs (D-ID, HeyGen, Synthesia)**: Export the generated script and audio, then call the provider’s API to render talking-head clips. Store API keys next to the OpenAI secrets and wrap calls in a separate module to keep vendor dependencies optional.

