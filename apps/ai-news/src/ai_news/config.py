# src/ai_news/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    openai_api_key: str
    openai_model: str
    openai_tts_model: str
    news_default_topic: str
    outputs_dir: str = "outputs"
    scripts_dir: str = "outputs/scripts"
    audio_dir: str = "outputs/audio"
    video_dir: str = "outputs/video"
    background_image_path: str = "assets/background.png"
    avatar_image_path: str = "assets/avatar.png"


def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

    return Settings(
        openai_api_key=api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        openai_tts_model=os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        news_default_topic=os.getenv("NEWS_DEFAULT_TOPIC", "AI and Tech News"),
    )
