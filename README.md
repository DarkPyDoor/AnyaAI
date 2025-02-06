# 🎙️ Anya AI v0.0.2 - Voice Assistant with Superpowers

A cutting-edge voice assistant that combines AI capabilities with system control features. Built with Python 3.10 and powered by modern AI models.

**Anya is in beta testing!**\
She still has a lot to learn. Later, I will create a list of her full capabilities and what will be added in the future.

## Choose Language

## 🌟 Features

- Voice-controlled computer operations
- AI-powered natural language understanding
- Code generation and execution
- Real-time weather/time information
- Web scraping capabilities
- Multi-language support
- Audio feedback system

## 🔄 Update v0.0.2

### What's New?
- Changed TTS model provider from `https://ttsmp3.com/` to `https://ttsopenai.com/`.
- Now there is **unlimited** text-to-speech usage instead of a **1000-character** daily limit.
- A unified authentication token is used—please **do not modify** the request type, such as changing `voice_id` or `model`.

## 🚀 Quick Start

### Requirements

- Python 3.10+ [Download](https://www.python.org/downloads/)
- FFmpeg ([Installation Guide](#-ffmpeg-installation))

### Installation

1. Clone repository:

```bash
git clone https://github.com/DarkPyDoor/AnyaAI.git
```

2. Setting Up FFmpeg Paths\
   To configure the paths for `ffmpeg.exe` and `ffprobe.exe`, modify the following lines in the file `core/tts.py`:

```python
# Setting FFmpeg paths
AudioSegment.ffmpeg = r"C:\path\to\your\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\path\to\your\ffmpeg\bin\ffprobe.exe"
AudioSegment.converter = AudioSegment.ffmpeg
```

3. Run the setup script:

```bat
start.bat
```

3.1 To start the assistant:

```bat
start.bat
```

### FFmpeg Installation

#### Windows

1. Download from [official site](https://ffmpeg.org/download.html#build-windows)
2. Add to PATH:
   - Right-click "This PC" → Properties → Advanced system settings
   - Environment Variables → Select "Path" → Edit → Add FFmpeg bin folder

## 🛠️ Usage

Activate the assistant using wake words:

- "Anya"
- "Аня"
- "Anya, please..."

Example commands:

```bash
"Open Chrome browser"
"What's the weather today?"
"Create a new Python script"
"Search for AI news"
```

**Need help?**\
Open an [issue](https://github.com/DarkPyDoor/AnyaAI/issues)

## 🔮 Future Plans
- Ability to interact with AI and interrupt its speech
- Change AI personality
- User-friendly interface for both PC and Android (Linux is uncertain for now)
- Conversation history
- Screen interaction
- PC control at the Python code level (**✅ Implemented**)
- Web search functionality
- Multi-language support
- User notifications
- AI-initiated conversation without disturbing active tasks (e.g., gaming)
- Improved voice perception
- Voice identification

And all of this will be **free**! 🎉

If you enjoy using Anya AI, please consider buying me some sweets via Binance Pay: **ID 438 485 773** 🍬

