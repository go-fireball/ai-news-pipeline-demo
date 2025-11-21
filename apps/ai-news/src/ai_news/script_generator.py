# src/ai_news/script_generator.py
import datetime
import os
from pathlib import Path
from typing import Tuple

from openai import OpenAI

from config import get_settings


def generate_news_script(topic: str | None = None) -> Tuple[str, str]:
    """
    Returns (script_text, script_path).
    """
    settings = get_settings()
    topic = topic or settings.news_default_topic

    client = OpenAI(api_key=settings.openai_api_key)

    today_str = datetime.datetime.now().strftime("%B %d, %Y")

    system_msg = (
        "You are a professional news anchor writing a spoken news script. "
        "Use simple, conversational English and short sentences. "
        "Assume this will be read aloud by an AI avatar on YouTube."
    )

    user_msg = f"""
Create a 2–3 minute spoken news script about today's {topic} as of {today_str}.

Requirements:
- Start with a short hook (1–2 sentences) addressing the viewer.
- Then present 2–4 major stories with smooth transitions.
- Use present tense and spoken style. Avoid long sentences.
- End with a brief outro inviting the viewer to come back for more updates.
- Do NOT include stage directions or camera cues. Only spoken lines.
- Include a short title line at the very top prefixed with: TITLE:
"""

    completion = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
    )

    full_text = completion.choices[0].message.content.strip()

    # Extract title line
    lines = full_text.splitlines()
    title_line = lines[0] if lines else "AI News Update"
    if title_line.upper().startswith("TITLE:"):
        title = title_line.split(":", 1)[1].strip()
        script_body = "\n".join(lines[1:]).strip()
    else:
        title = "AI News Update"
        script_body = full_text

    # Save to file
    Path(settings.scripts_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"news_{timestamp}.txt"
    script_path = os.path.join(settings.scripts_dir, filename)

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"TITLE: {title}\n\n{script_body}")

    return script_body, script_path
