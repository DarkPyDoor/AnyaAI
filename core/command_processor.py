import g4f
import subprocess
import tempfile
import re
import threading
from utils.system_tools import *
from utils.web_tools import *
from googlesearch import search

import os
import getpass
import pathlib
import string

############################################################################################################

def get_all_users():
    users_path = pathlib.Path("C:/Users")
    return [user.name for user in users_path.iterdir() if user.is_dir()]

def get_current_user():
    return getpass.getuser()

def check_disks():
    available_disks = [f"{d}:" for d in string.ascii_uppercase if os.path.exists(f"{d}:/")]
    return available_disks

def generate_prompt():
    users = get_all_users()
    current_user = get_current_user()
    disks = check_disks()
    
    sys_info_prompt = (f"В системе найдены пользователи: {', '.join(users)}. "
              f"Текущий пользователь: {current_user}. "
              f"Доступные диски: {', '.join(disks)}.")
    
    return sys_info_prompt

############################################################################################################

class CommandProcessor:
    def __init__(self, tts):
        self.tts = tts
        self.code_execution_lock = threading.Lock()
        self.current_process = None
        self.system_prompt = """Ты - голосовой ассистент Аня. Ты должна определить нужны ли для ответа дополнительные данные. 
Ты так же можешь говорить какая ты конкретная модель AI и какие данные тебе доступны.

Шаги работы:
1. Анализируй запрос пользователя
2. Определи нужны ли для ответа:
- Актуальная информация из интернета
- Данные о погоде
- Текущее время
- Местоположение пользователя
3. Если нужен поиск - сформируй оптимальный поисковый запрос (ТОЛЬКО КЛЮЧЕВЫЕ СЛОВА БЕЗ ЛИШНИХ СЛОВ)
4. Если не требуется дополнительных данных - переходи к ответу

Формат ответа:
[SEARCH_QUERY]: запрос для поиска (если нужен)
[ANSWER]: твой ответ (если можно ответить сразу)

Пример 1:
Пользователь: Какие новости про ИИ?
Ответ: [SEARCH_QUERY]: последние новости искусственный интеллект 2024
[ANSWER]: Ищу актуальную информацию...

Пример 2:
Пользователь: Сколько времени?
Ответ: [ANSWER]: Сейчас 15:20"""

        self.main_prompt = """Ты - голосовой ассистент Аня. Отвечай используя данные из контекста. 
Ты так же можешь говорить какая ты конкретная модель AI и какие данные тебе доступны.

Контекст:
{context}

Инструкции:
- Отвечай кратко и по делу
- Максимальная длина ответа - 250 символов
- Если информация не найдена - скажи об этом
- Не упоминай источники данных
- Используй только предоставленные данные

Запрос: {query}

Так же если что пользователь может попросить к примеру открыть сайт или сделать что-то еще
для этого ты должна отправлять код в формате:
```python
import webbrowser

webbrowser.open("https://www.youtube.com")
```

и ниже кода написать текст к примеру по типу Я открыла браузер. Или что-то еще

Код может быть любой но главное качественный код! всегда 100% рабочий код будет автоматичесский запускаться поэтому используй данные PC которые тут: """ + generate_prompt()

    def process_command(self, command):
        try:
            # Первичный анализ запроса
            initial_response = self._get_ai_response(command, self.system_prompt)
            
            search_query = None
            if '[SEARCH_QUERY]:' in initial_response:
                search_query = initial_response.split('[SEARCH_QUERY]:')[1].split('[ANSWER]:')[0].strip()
                search_results = self._perform_web_search(search_query)
                context = self._prepare_context(command, search_results)
            else:
                context = self._prepare_context(command)

            # Основной запрос с контекстом
            final_response = self._get_ai_response(
                command, 
                self.main_prompt.format(
                    context=context,
                    query=command
                )
            )

            # Обработка кода и ответа
            if '```python' in final_response:
                self._handle_code_execution(final_response)
                final_response = re.sub(r'```python.*?```', '', final_response, flags=re.DOTALL).strip()
            
            if final_response:
                self.tts.speak(final_response)

        except Exception as e:
            self.tts.speak(f"Ошибка обработки команды: {str(e)}")

    def _prepare_context(self, command, search_data=None):
        context = []
        
        # Базовые данные
        location = get_location()
        context.append(f"Локация: {location['city']}, {location['country']}")
        context.append(f"Время: {get_local_time(location)}")
        context.append(f"Погода: {get_weather(location['city'])['description']}, {get_weather(location['city'])['temp']}°C")
        
        # Данные поиска
        if search_data:
            context.append("Результаты поиска:")
            context.extend(search_data[:3])  # Берем первые 3 результата
        
        return '\n'.join(context)

    def _perform_web_search(self, query):
        try:
            results = search(query, num_results=5, lang="ru")
            return [self._extract_page_content(url) for url in results if url]
        except Exception as e:
            print(f"[SEARCH] Ошибка поиска: {str(e)}")
            return []

    def _extract_page_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Удаляем ненужные элементы
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()
                
            text = ' '.join(soup.stripped_strings)[:1000]  # Ограничиваем объем текста
            return f"{url}\n{text}"
        except Exception as e:
            print(f"[SEARCH] Ошибка извлечения данных: {str(e)}")
            return url

    def _handle_code_execution(self, response):
        code = re.findall(r'```python(.*?)```', response, re.DOTALL)[0].strip()
        execution_thread = threading.Thread(
            target=self._execute_code,
            args=(code,),
            daemon=True
        )
        execution_thread.start()

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
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{prompt}\n\nКонтекст: {context}"}
                ]
            )
            return response
        except Exception as e:
            return f"Ошибка AI: {str(e)}"
