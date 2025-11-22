# src/ai_news/main.py
import argparse
import os

from config import get_settings
from script_generator import generate_news_script
from tts import synthesize_speech
from video_builder import build_simple_video


def run_pipeline(topic: str | None = None) -> None:
    settings = get_settings()

    print("=== AI News Pipeline ===")
    if topic:
        print(f"Topic: {topic}")
    else:
        print(f"Topic: {settings.news_default_topic} (default)")

    # 1. Generate script
    print("\n[1/2] Generating script...")
    script_text, script_path = generate_news_script(topic)
    print(f"Script saved to: {script_path}")

    # 2. Synthesize speech
    print("\n[2/3] Generating narration audio...")
    audio_path = synthesize_speech(script_text)
    print(f"Audio saved to: {audio_path}")

    # Extract a title from script file (first line starting with TITLE)
    title = "AI News Update"
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line.upper().startswith("TITLE:"):
            title = first_line.split(":", 1)[1].strip()
    except Exception:
        pass

    # 3. Build video
    print("\n[3/3] Building video...")
    video_path = build_simple_video(audio_path, title=title)
    print(f"Video saved to: {video_path}")

    print("\n✅ Done! You can now open the video file and watch your AI newsreader.")


def main():
    parser = argparse.ArgumentParser(description="AI News Video Pipeline")
    parser.add_argument(
        "--topic",
        type=str,
        help="Topic for the news (e.g., 'AI and Tech News', 'Stock Market Today')",
    )
    args = parser.parse_args()

    run_pipeline(topic="Ai Stock news")


if __name__ == "__main__":
    main()
