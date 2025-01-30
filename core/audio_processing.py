import speech_recognition as sr
import threading
import traceback

class AudioProcessor:
    def __init__(self, tts, processor, trigger_words):
        self.tts = tts
        self.processor = processor
        self.trigger_words = trigger_words
        self.listening = False
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.lock = threading.Lock()

    def stop_all_operations(self):
        if self.processor.current_process:
            try:
                self.processor.current_process.terminate()
                print("[AUDIO] Выполнение кода прервано")
            except Exception as e:
                print(f"[AUDIO] Ошибка прерывания процесса: {str(e)}")

    def start_listening(self):
        print("[AUDIO] Запуск процесса прослушивания")
        if not self.tts.is_ready():
            print("[AUDIO] TTS сервис не готов!")
            
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("[AUDIO] Калибровка шумов завершена")
            
        while True:
            try:
                print("[AUDIO] Ожидание фразы...")
                with self.mic as source:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
                text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                print(f"[AUDIO] Распознано: '{text}'")

                if any(trigger in text for trigger in self.trigger_words):
                    print("[AUDIO] Обнаружено триггерное слово")
                    with self.lock:
                        self.tts.stop_playing()
                        print("[AUDIO] Запуск обработки команды")
                        self.processor.process_command(text)
                        
            except sr.WaitTimeoutError:
                print("[AUDIO] Таймаут ожидания фразы")
            except sr.UnknownValueError:
                print("[AUDIO] Не удалось распознать речь")
            except sr.RequestError as e:
                print(f"[AUDIO] Ошибка сервиса распознавания: {str(e)}")
            except Exception as e:
                print(f"[AUDIO] Критическая ошибка:")
                traceback.print_exc()
                