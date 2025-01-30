from core.audio_processing import AudioProcessor
from core.tts import TextToSpeech
from core.command_processor import CommandProcessor
import threading
import time

# Если нужно перевести отладочные сообщения, делайте это вручную. | If you need to translate debug messages, do it manually.
# Я не планирую переводить их до выхода релизной версии. | I don't plan to translate them until the release version is released.

def main():
    print("[MAIN] Запуск приложения...")
    tts = TextToSpeech()
    
    if not tts.is_ready():
        print("[MAIN] Ошибка инициализации TTS! Приложение не может работать")
        return
    
    processor = CommandProcessor(tts)
    
    audio_processor = AudioProcessor(
        tts=tts,
        processor=processor,
        trigger_words=['Аня', 'аня', 'Anya', 'ANYA', 'Аня.', 'аня'] # (Слова-триггеры для активации ассистента, можно добавить свои | Trigger words for activating the assistant, you can add your own)
    )
    
    audio_thread = threading.Thread(target=audio_processor.start_listening, daemon=True)
    audio_thread.start()
    print("[MAIN] Приложение успешно запущено и работает")

    try:
        while audio_thread.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[MAIN] Завершение работы...")
    finally:
        tts.stop_playing()
        audio_processor.stop_all_operations()

if __name__ == "__main__":
    main()