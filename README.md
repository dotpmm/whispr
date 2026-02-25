# Whisper Keybind Daemon

A lightweight Python script that lets you transcribe speech to your clipboard using a global keyboard shortcut, powered by OpenAI's Whisper (via `faster-whisper`).

## Features

- **Global Hotkey:** Works anywhere in your OS.
- **Local Processing:** Runs entirely on your CPU using `int8` quantization.
- **Auto-Copy:** Transcribed text is automatically placed in your clipboard.
- **Simple Setup:** Configures your preferred keybind on the first run.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Requires `portaudio` (Windows) or `libportaudio2` (Linux) for `sounddevice`.*

## Usage

Run the script:
```bash
python main.py
```

On the first run, it will ask you to press the key combination you want to use (e.g., `Ctrl + Alt + R`). After that:
1. Press your hotkey to **start** recording.
2. Press it again to **stop**.
3. Wait a moment for transcription to finish and paste the result!

## Configuration

Settings are stored in `~/.whisper_keybind_config.json`. Delete this file if you want to change your hotkey.

