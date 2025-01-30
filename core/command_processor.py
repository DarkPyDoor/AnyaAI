import g4f
import subprocess
import tempfile
import re
import threading
from utils.system_tools import *
from utils.web_tools import *

class CommandProcessor:
    def __init__(self, tts):
        self.tts = tts
        self.code_execution_lock = threading.Lock()
        self.current_process = None
        self.system_prompt = """Ты - голосовой ассистент Ния. Ты должна помогать пользователю с:
1. Управлением компьютером через Python код (генерируй код в ```python блоках)
2. Ответами на общие вопросы
3. Получением информации о местоположении, времени и погоде

Инструкции:
- Для управления ПК генерируй код используя библиотеки: pyautogui, pygetwindow, webbrowser, os, time
- Всегда проверяй безопасность кода перед выполнением
- Отвечай кратко и дружелюбно
- Максимальная длина ответа для озвучки - 220 символов

Доступные функции:
- get_location() → {city, country, coordinates}
- get_weather(city) → {temp, description}
- get_time() → текущее время
- web_search(query) → результаты поиска

Ты не должна говорить фразы по типу:
'Конечно! Вот код для запуска браузера:



Этот код откроет Google в вашем браузере по умолчанию. 😊'


Ты должна говорить:

Браузер открыт! 

Не используй смайлики!
"""

    def process_command(self, command):
        try:
            context = self._gather_context(command)
            response = self._get_ai_response(command, context)
            
            if '```python' in response:
                code = re.findall(r'```python(.*?)```', response, re.DOTALL)[0].strip()
                execution_thread = threading.Thread(
                    target=self._execute_code,
                    args=(code,),
                    daemon=True
                )
                execution_thread.start()
                
                response = re.sub(r'```python.*?```', '', response, flags=re.DOTALL).strip()
            
            if response:
                self.tts.speak(response)
                
        except Exception as e:
            self.tts.speak(f"Ошибка обработки команды: {str(e)}")

    def _execute_code(self, code):
        with self.code_execution_lock:
            try:
                with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp:
                    tmp.write(code.encode())
                    tmp_name = tmp.name
                
                self.current_process = subprocess.Popen(
                    ['python', tmp_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                output_thread = threading.Thread(
                    target=self._monitor_process_output,
                    args=(self.current_process, tmp_name),
                    daemon=True
                )
                output_thread.start()

            except Exception as e:
                print(f"[EXEC] Ошибка выполнения кода: {str(e)}")

    def _monitor_process_output(self, process, tmp_path):
        try:
            while process.poll() is None:
                output = process.stdout.readline()
                if output:
                    print(f"[EXEC] Вывод: {output.strip()}")
                
                error = process.stderr.readline()
                if error:
                    print(f"[EXEC] Ошибка: {error.strip()}")

            final_output, final_error = process.communicate()
            if final_output:
                print(f"[EXEC] Финальный вывод: {final_output.strip()}")
            if final_error:
                print(f"[EXEC] Финальные ошибки: {final_error.strip()}")

        finally:
            try:
                os.unlink(tmp_path)
            except Exception as e:
                print(f"[EXEC] Ошибка удаления файла: {str(e)}")

    def _gather_context(self, command):
        context = {}
        if any(word in command for word in ['погод', 'времен']):
            location = get_location()
            context['location'] = location
            context['weather'] = get_weather(location['city'])
            context['time'] = get_local_time(location)
        return context

    def _get_ai_response(self, prompt, context):
        try:
            response = g4f.ChatCompletion.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{prompt}\n\nКонтекст: {context}"}
                ]
            )
            return response
        except Exception as e:
            return f"Ошибка AI: {str(e)}"