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

def web_search(query, num_results=5):
    try:
        return list(search(query, num_results=num_results, lang="ru"))
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return []
