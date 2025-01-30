import ipinfo
import requests
from datetime import datetime
import subprocess
import mss
import os

def open_application(app_name):
    try:
        if os.name == 'nt':
            os.startfile(app_name)
        else:
            subprocess.Popen([app_name], start_new_session=True) # (Это для Linux, не трогать ещё не работает! | This is for Linux, do not touch it does not work yet!)
        return True
    except Exception as e:
        print(f"[SYSTEM] Ошибка открытия приложения: {str(e)}")
        return False

def get_location():
    try:
        handler = ipinfo.getHandler('7f67ce0865ca4a')
        details = handler.getDetails()
        return {
            'city': details.city,
            'country': details.country_name,
            'coordinates': (details.latitude, details.longitude)
        }
    except:
        return {'city': 'Неизвестно', 'country': 'Неизвестно'}

def get_weather(city):
    try:
        api_key = "ВАШ_OPENWEATHERMAP_API" # (Не трогать это будет позже в новых обновлениях! | Do not touch this will be in new updates!)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    except:
        return {'temp': 'Неизвестно', 'description': 'Нет данных'}

def get_local_time(location):
    return datetime.now().strftime("%H:%M")

def take_screenshot():
    with mss.mss() as sct:
        filename = os.path.join(tempfile.gettempdir(), "screenshot.png")
        sct.shot(output=filename)
        return filename

