import requests
import hashlib
import os
import simpleaudio as sa
from pathlib import Path
import traceback
from pydub import AudioSegment
import subprocess
import tempfile
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Настройка путей FFmpeg
AudioSegment.ffmpeg = r"C:\путь\к\вашему\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\путь\к\вашему\ffmpeg\bin\ffprobe.exe"
AudioSegment.converter = AudioSegment.ffmpeg

class TextToSpeech:
    def __init__(self):
        self.temp_dir = Path("temp_audio")
        self.temp_dir.mkdir(exist_ok=True)
        
        self.cache_dir = Path("tts_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        self.current_playback = None
        self.initialized = False
        self.session = self._create_retry_session()
        
        print("[TTS] Инициализация TextToSpeech...")
        self._initialize_audio_system()

    def _create_retry_session(self):
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            allowed_methods=frozenset(['POST', 'GET'])
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _initialize_audio_system(self):
        try:
            test_file = self.temp_dir / "test_audio.wav"
            test_audio = AudioSegment.silent(duration=100)
            test_audio.export(test_file, format="wav")
            
            if test_file.exists():
                print("[TTS] FFmpeg работает корректно")
                self.initialized = True
                test_file.unlink()
            else:
                print("[TTS] Ошибка проверки FFmpeg")

        except Exception as e:
            print(f"[TTS] Ошибка инициализации: {str(e)}")
            traceback.print_exc()

    def _convert_to_wav(self, mp3_data):
        for attempt in range(3):
            try:
                with tempfile.NamedTemporaryFile(dir=self.temp_dir, suffix=".mp3", delete=False) as tmp_mp3:
                    tmp_mp3.write(mp3_data)
                    mp3_path = tmp_mp3.name

                wav_path = Path(self.temp_dir) / f"{Path(mp3_path).stem}.wav"

                command = [
                    AudioSegment.ffmpeg,
                    '-y',
                    '-i', mp3_path,
                    '-acodec', 'pcm_s16le',
                    '-ar', '44100',
                    '-ac', '1',
                    str(wav_path)
                ]

                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                if result.returncode != 0:
                    print(f"[TTS] Ошибка конвертации (попытка {attempt+1}):\n{result.stderr.decode()}")
                    continue

                with open(wav_path, 'rb') as f:
                    wav_data = f.read()

                return wav_data

            except Exception as e:
                print(f"[TTS] Ошибка конвертации (попытка {attempt+1}): {str(e)}")
                traceback.print_exc()
            
            finally:
                for path in [mp3_path, wav_path]:
                    try:
                        if path and Path(path).exists():
                            os.unlink(path)
                    except Exception as e:
                        print(f"[TTS] Ошибка очистки файлов: {str(e)}")

        return None

    def generate_tts(self, text):
        if not self.initialized:
            return None

        print(f"[TTS] Генерация TTS для: '{text}'")
        cache_key = hashlib.md5(text.encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.mp3"
        
        if cache_file.exists():
            print(f"[TTS] Использование кэша: {cache_file}")
            return cache_file.read_bytes()
        
        try:
            response = self.session.post(
                "https://ttsmp3.com/makemp3_ai.php",
                headers={
                    "content-type": "application/x-www-form-urlencoded",
                    "referer": "https://ttsmp3.com/ai",
                },
                data={
                    "msg": text,
                    "lang": "nova",
                    "speed": "1.00",
                    "source": "ttsmp3"
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("Error") == 0:
                    mp3_url = f"https://ttsmp3.com/created_mp3_ai/{result['MP3']}"
                    mp3_data = self.session.get(mp3_url, timeout=10).content
                    if len(mp3_data) > 0:
                        cache_file.write_bytes(mp3_data)
                        return mp3_data

            print(f"[TTS] Ошибка API: {response.text}")
            return None

        except Exception as e:
            print(f"[TTS] Ошибка генерации:")
            traceback.print_exc()
            return None

    def speak(self, text):
        if not self.initialized:
            return

        try:
            mp3_data = self.generate_tts(text)
            if mp3_data:
                wav_data = self._convert_to_wav(mp3_data)
                if wav_data:
                    self.stop_playing()
                    self.current_playback = sa.play_buffer(
                        wav_data,
                        num_channels=1,
                        bytes_per_sample=2,
                        sample_rate=44100
                    )
                    print("[TTS] Воспроизведение успешно запущено")

        except Exception as e:
            print(f"[TTS] Ошибка воспроизведения:")
            traceback.print_exc()

    def stop_playing(self):
        if self.current_playback:
            try:
                if self.current_playback.is_playing():
                    print("[TTS] Остановка воспроизведения")
                    self.current_playback.stop()
            except Exception as e:
                print(f"[TTS] Ошибка остановки воспроизведения: {str(e)}")
            finally:
                self.current_playback = None

    def is_ready(self):
        return self.initialized

    def __del__(self):
        self.stop_playing()
        for file in self.temp_dir.glob("*"):
            try:
                file.unlink()
            except Exception as e:
                print(f"[TTS] Ошибка очистки файлов: {str(e)}")