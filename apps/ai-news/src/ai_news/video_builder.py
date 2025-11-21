# src/ai_news/video_builder.py
import datetime
import os
from pathlib import Path

from moviepy import AudioFileClip, ImageClip

from config import get_settings


def build_simple_video(audio_path: str, title: str | None = None) -> str:
    """
    Creates a simple video: static background + narration.
    Returns the video file path.
    """
    settings = get_settings()

    if not os.path.exists(settings.avatar_image_path):
        raise FileNotFoundError(
            f"Background image not found at {settings.avatar_image_path}"
        )
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    Path(settings.video_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = (title or "ai_news_update").replace(" ", "_")[:40]
    video_filename = f"{safe_title}_{timestamp}.mp4"
    video_path = os.path.join(settings.video_dir, video_filename)

    # Load audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Create image clip
    image_clip = ImageClip(settings.avatar_image_path, duration=duration)

    # Combine
    image_clip.audio = audio_clip
    image_clip.write_videofile(
        video_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4,
    )

    # Close resources
    audio_clip.close()
    image_clip.close()
    return video_path
