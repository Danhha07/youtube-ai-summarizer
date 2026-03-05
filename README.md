# YouTube AI Summarizer

Free AI tool that summarizes YouTube videos using local AI (Ollama).

## Features

- Fetch transcript from YouTube
- Summarize video using local AI
- Export summary to Markdown file
## Requirements

- Python 3
- Ollama
- llama3 model

## Setup

Clone repository:

```bash
git clone https://github.com/Danhha07/youtube-ai-summarizer.git
cd youtube-ai-summarizer
pip install -r requirements.txt
ollama serve
ollama pull llama3
python app.py
