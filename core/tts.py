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
        self.auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg4OTM2MzYsInN1YiI6IjBkYjE3YzJhLWU0MmUtMTFlZi1iY2Q5LTFlYjg2OGU2ZmUzYSJ9.ewFLTpNqs9w3lqDm7Xrv6IBanhEgF4gl3DJzZZscuus"
        
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

    def _get_media_url(self, uuid):
        for attempt in range(6):  # 6 попыток с интервалом 1 секунда
            try:
                response = self.session.get(
                    f"https://api.ttsopenai.com/api/v1/history/{uuid}",
                    headers={
                        "authorization": f"Bearer {self.auth_token}",
                        "accept": "application/json",
                        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"Windows"',
                    },
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 2 and data.get('media_url'):
                        return data['media_url']
                    print(f"[TTS] Попытка {attempt+1}/6: Статус генерации {data.get('status_percentage')}%")
                else:
                    print(f"[TTS] Ошибка получения статуса (HTTP {response.status_code})")

            except Exception as e:
                print(f"[TTS] Ошибка запроса статуса (попытка {attempt+1}/6): {str(e)}")

            time.sleep(1)  # Задержка 1 секунда между попытками

        print("[TTS] Превышено максимальное количество попыток")
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
            # Шаг 1: Создание TTS задачи
            response = self.session.post(
                "https://api.ttsopenai.com/api/v1/text-to-speech-stream",
                headers={
                    "authorization": f"Bearer {self.auth_token}",
                    "content-type": "application/json",
                    "accept": "application/json",
                    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                },
                json={
                    "model": "tts-1",
                    "speed": 1,
                    "input": text,
                    "voice_id": "OA005"
                },
                timeout=15
            )

            if response.status_code != 200:
                print(f"[TTS] Ошибка API (HTTP {response.status_code}): {response.text}")
                return None

            task_data = response.json()
            uuid = task_data.get('uuid')
            if not uuid:
                print("[TTS] Не удалось получить UUID задачи")
                return None

            # Шаг 2: Получение ссылки на аудио
            media_url = self._get_media_url(uuid)
            if not media_url:
                print("[TTS] Не удалось получить ссылку на аудио")
                return None

            # Шаг 3: Скачивание аудио
            mp3_data = self.session.get(media_url, timeout=15).content
            if len(mp3_data) > 0:
                cache_file.write_bytes(mp3_data)
                return mp3_data

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
