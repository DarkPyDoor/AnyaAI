# 🎙️ Anya AI v0.0.3 - Voice Assistant with Superpowers

A cutting-edge voice assistant that combines AI capabilities with system control features. Built with Python 3.10 and powered by modern AI models.

**Anya is in beta testing!**\
She still has a lot to learn. Later, I will create a list of her full capabilities and what will be added in the future.

<!-- Copy-paste in your Readme.md file -->

<a href="https://next.ossinsight.io/widgets/official/compose-activity-trends?repo_id=924429727" target="_blank" style="display: block" align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://next.ossinsight.io/widgets/official/compose-activity-trends/thumbnail.png?repo_id=924429727&image_size=auto&color_scheme=dark" width="815" height="auto">
    <img alt="Activity Trends of DarkPyDoor/AnyaAI - Last 28 days" src="https://next.ossinsight.io/widgets/official/compose-activity-trends/thumbnail.png?repo_id=924429727&image_size=auto&color_scheme=light" width="815" height="auto">
  </picture>
</a>

<!-- Made with [OSS Insight](https://ossinsight.io/) -->

## Choose Language
[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Russian](https://img.shields.io/badge/Language-Russian-red)](README_ru.md)

## 🌟 Features

- Voice-controlled computer operations
- AI-powered natural language understanding
- Code generation and execution
- Real-time weather/time information
- Web scraping capabilities
- Multi-language support
- Audio feedback system

## 🔄 Update v0.0.3

### What's New?
- Improved AI prompt engineering for better responses.
- Switched AI model from `deepseek-chat` to `gpt-4o`.
- Implemented **web search functionality**.
- **Known Issue:** The `bearer token` for `ttsopenai` expires every few hours. Until this is resolved, please manually update the token in `utils/tts.py` (line 30).\
  **How to get a new Bearer Token:**
  1. Go to `https://ttsopenai.com/`
  2. Open Developer Console (F12)
  3. Generate an audio request on the website
  4. Find the `text-to-speech-stream` request in Network tab
  5. Copy the `authorization: Bearer <token>` from request headers

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
- Web search functionality (**✅ Implemented**)
- Multi-language support
- User notifications
- AI-initiated conversation without disturbing active tasks (e.g., gaming)
- Improved voice perception
- Voice identification
- **Add vocal pauses like ['uhhh', 'ummm', 'hmm', 'well...'] to eliminate unnatural silence**

And all of this will be **free**! 🎉

If you enjoy using Anya AI, please consider buying me some sweets via Binance Pay: **ID 438 485 773** 🍬

