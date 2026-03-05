import re
from datetime import datetime
from pathlib import Path

import requests
from youtube_transcript_api import YouTubeTranscriptApi

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def extract_video_id(s: str) -> str:
    s = s.strip()

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s

    patterns = [
        r"v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"shorts/([A-Za-z0-9_-]{11})",
    ]

    for p in patterns:
        m = re.search(p, s)
        if m:
            return m.group(1)

    raise ValueError("Không tìm thấy video id.")


from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def fetch_transcript(video_id: str) -> str:
    try:
        # Lấy transcript ưu tiên vi -> en
        items = YouTubeTranscriptApi.get_transcript(video_id, languages=["vi", "en"])
        return " ".join([x["text"] for x in items]).strip()

    except (TranscriptsDisabled, NoTranscriptFound):
        raise RuntimeError("Video này không có transcript hoặc đã tắt phụ đề.")

    except VideoUnavailable:
        raise RuntimeError("Video không khả dụng / bị giới hạn khu vực / cần đăng nhập.")

    except Exception as e:
        raise RuntimeError(f"Không lấy được transcript. Chi tiết: {e}") from e


def summarize_with_ollama(transcript: str) -> str:

    transcript_cut = transcript[:18000]

    prompt = f"""
Bạn là trợ lý tóm tắt video YouTube. Trả lời bằng tiếng Việt theo Markdown:

## Tóm tắt nhanh
- ...

## Các ý chính
- [ ] ...

## Từ khóa
- ...

Transcript:
{transcript_cut}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=600)
    r.raise_for_status()

    return r.json()["response"].strip()


def save_md(video_id: str, md: str) -> str:

    Path("outputs").mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    path = Path("outputs") / f"{video_id}_{ts}.md"

    path.write_text(md, encoding="utf-8")

    return str(path)


def main():

    print("=== YouTube AI Summarizer (FREE - Ollama) ===")

    s = input("Dán link YouTube hoặc video id: ").strip()

    video_id = extract_video_id(s)

    print("Video ID:", video_id)

    print("1) Lấy transcript...")
    transcript = fetch_transcript(video_id)

    print("2) Tóm tắt bằng Ollama...")
    summary = summarize_with_ollama(transcript)

    out = save_md(video_id, summary)

    print("✅ Xong! File:", out)


if __name__ == "__main__":
    main()

