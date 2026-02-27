from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
CACHE_DIR = os.environ.get("WHISPER_CACHE", None)

@app.on_event("startup")
async def load_model():
    global model
    from faster_whisper import WhisperModel
    print("INFO:     Loading Whisper model")
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
        download_root=CACHE_DIR,
    )
    print("INFO:     Whisper model ready.")

@app.get("/", response_class=HTMLResponse)
async def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content, media_type="text/html; charset=utf-8")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse({"error": "Model not loaded yet"}, status_code=503)

    audio_bytes = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        segments, _ = model.transcribe(tmp_path, beam_size=5, language="en")
        text = "\n".join(seg.text.strip() for seg in segments if seg.text.strip())
        return JSONResponse({"text": text or ""})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        os.unlink(tmp_path)