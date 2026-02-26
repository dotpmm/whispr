---
title: Whispr
emoji: 🎙️
colorFrom: yellow
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# Whispr

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/dotpmm/whispr)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Python](https://img.shields.io/badge/python-3.11+-blue?logo=python)
![Whisper](https://img.shields.io/badge/whisper-base-green?logo=openai)

A web-based speech transcription service powered by OpenAI's Whisper model. Upload audio and get instant text transcription.

## 🚀 Try it live

**Live demo:** https://huggingface.co/spaces/dotpmm/whispr

## How it works

- **FastAPI backend** serves a web interface and transcription API
- **Whisper model** (base, int8) runs locally on CPU for privacy
- **Web interface** lets you record or upload audio files
- **REST API** at `/transcribe` accepts audio uploads

## Quick start

**Run locally:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Or with Docker:**
```bash
docker build -t whispr .
docker run -p 7860:7860 whispr
```

Open http://localhost:7860 and start transcribing!

