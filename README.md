# 🎙️ Anya AI - Voice Assistant with Superpowers

[![Python 3.10](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)

A cutting-edge voice assistant that combines AI capabilities with system control features. Built with Python 3.10 and powered by modern AI models.

**Anya is in beta testing!**  
She still has a lot to learn. Later, I will create a list of her full capabilities and what will be added in the future.

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

## 🚀 Quick Start

### Requirements
- Python 3.10+ [Download](https://www.python.org/downloads/)
- FFmpeg ([Installation Guide](#-ffmpeg-installation))

### Installation
1. Clone repository:
```bash
git clone https://github.com/DarkPyDoor/AnyaAI.git
```

2. Setting Up FFmpeg Paths  
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

# AnyaAI was not tested in English!


**Need help?**  
Open an [issue](https://github.com/DarkPyDoor/AnyaAI/issues)
