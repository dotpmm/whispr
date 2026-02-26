FROM python:3.11-slim

ENV PORT=7860
ENV HOST=0.0.0.0

ENV WHISPER_CACHE=/app/.cache
ENV HF_HOME=/app/.cache

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cpu', compute_type='int8', download_root='/app/.cache')"

COPY main.py .
COPY index.html .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]