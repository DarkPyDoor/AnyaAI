import requests
from bs4 import BeautifulSoup
import ipinfo

def get_location():
    try:
        handler = ipinfo.getHandler(access_token='7f67ce0865ca4a')
        details = handler.getDetails()
        return {
            'city': details.city,
            'country': details.country_name,
            'latitude': details.latitude,
            'longitude': details.longitude
        }
    except Exception as e:
        print(f"Ошибка получения локации: {str(e)}")
        return None

def get_web_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return {
            'title': soup.title.string if soup.title else '',
            'content': soup.get_text()[:2000]
        }
    except Exception as e:
        print(f"Ошибка получения веб-контента: {str(e)}")
        return None