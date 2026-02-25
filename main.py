import json
import threading
import sys
from pathlib import Path

import numpy as np
import sounddevice as sd
import pyperclip
from pynput import keyboard
from faster_whisper import WhisperModel


CONFIG_PATH = Path.home() / ".whisper_keybind_config.json"
SAMPLE_RATE = 16000
WHISPER_MODEL = "base"

recording = False
audio_buffer = []
pressed_keys = set()
keybind = {}

def log(level, message):
    print(f"[{level}] {message}")

def first_time_setup():
    log("INFO", "First-time setup detected.")
    log("INFO", "Press the key combination you want to use to toggle recording.")

    captured = set()

    def on_press(key):
        captured.add(key)
        log("DEBUG", f"Key captured: {key}")

    def on_release(key):
        if captured:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    keys = []
    for k in captured:
        if isinstance(k, keyboard.Key):
            keys.append(k.name)
        else:
            keys.append(k.char)

    config = {"keybind": keys}

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    log("SUCCESS", f"Keybind saved: {' + '.join(keys)}")
    return config

def load_config():
    if not CONFIG_PATH.exists():
        return first_time_setup()

    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        return config
    except Exception as e:
        log("ERROR", f"Failed to load config: {e}")
        sys.exit(1)

def load_whisper():
    try:
        log("INFO", "Loading Whisper model...")
        return WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )
    except Exception as e:
        log("ERROR", f"Failed to load Whisper model: {e}")
        sys.exit(1)

model = load_whisper()

def audio_callback(indata, frames, time, status):
    if status:
        log("WARN", f"Audio stream warning: {status}")

    if recording:
        audio_buffer.append(indata.copy().flatten())

def transcribe_and_copy(audio_np):
    if audio_np.size == 0:
        log("WARN", "Recording was empty. Skipping transcription.")
        return

    try:
        log("INFO", "Transcribing audio...")
        segments, _ = model.transcribe(audio_np, beam_size=5, language="en")
        text = "\n".join(seg.text.strip() for seg in segments if seg.text.strip())

        if not text:
            log("WARN", "No speech detected.")
            return

        pyperclip.copy(text)

        log("SUCCESS", "Transcription completed and copied to clipboard.")
        print(f"\n{text}\n")

    except Exception as e:
        log("ERROR", f"Transcription failed: {e}")

def toggle_recording():
    global recording, audio_buffer

    if not recording:
        audio_buffer = []
        recording = True
        log("INFO", "Recording started.")
    else:
        recording = False
        log("INFO", "Recording stopped.")

        try:
            audio_np = np.concatenate(audio_buffer)
        except ValueError:
            log("WARN", "No audio data captured.")
            return

        threading.Thread(
            target=transcribe_and_copy,
            args=(audio_np,),
            daemon=True
        ).start()

def on_press(key):
    pressed_keys.add(key)

    normalized = set()
    for k in pressed_keys:
        if isinstance(k, keyboard.Key):
            normalized.add(k.name)
        else:
            normalized.add(k.char)

    if set(keybind["keybind"]).issubset(normalized):
        toggle_recording()
        pressed_keys.clear()

def on_release(key):
    pressed_keys.discard(key)

def main():
    global keybind

    keybind = load_config()

    log("INFO", "Whisper keybind daemon started.")
    log("INFO", f"Active keybind: {' + '.join(keybind['keybind'])}")

    try:
        stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=audio_callback
        )
        stream.start()
    except Exception as e:
        log("ERROR", f"Failed to access microphone: {e}")
        sys.exit(1)

    with keyboard.Listener(on_press=on_press, on_release=on_release):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            log("INFO", "Shutdown requested. Exiting cleanly.")
            sys.exit(0)

if __name__ == "__main__":
    main()
