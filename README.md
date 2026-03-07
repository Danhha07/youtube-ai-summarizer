# YouTube AI Summarizer

Free AI tool that summarizes YouTube videos using **local AI (Ollama)**.

## Features

- Fetch transcript from YouTube
- Summarize video using local LLM (llama3)
- Works fully offline with Ollama
- Export summary to Markdown file

## Requirements

- Python 3.10+
- Ollama
- llama3 model

Install Ollama model:

```bash
ollama pull llama3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama serve
python app.py
Input:
https://www.youtube.com/watch?v=xxxx

Output:
- Key ideas
- Summary
- Main takeaway
