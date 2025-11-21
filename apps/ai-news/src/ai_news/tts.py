# src/ai_news/tts.py
import datetime
import os
from pathlib import Path

from openai import OpenAI

from config import get_settings


def synthesize_speech(text: str, voice: str = "alloy") -> str:
    """
    Generate an MP3 audio file from the given text.
    Returns the audio file path.
    """
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    Path(settings.audio_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path = os.path.join(settings.audio_dir, f"news_{timestamp}.mp3")

    # Streaming TTS (official pattern from OpenAI docs)
    with client.audio.speech.with_streaming_response.create(
            model=settings.openai_tts_model,
            voice=voice,
            input=text,
    ) as response:
        response.stream_to_file(audio_path)

    return audio_path
