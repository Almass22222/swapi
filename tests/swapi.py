import requests
from requests import Response
import os


class APIRequester:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str = '', params: dict = None) -> Response:
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() 
            return response
        except requests.exceptions.RequestException as e:
            print("Возникла ошибка при выполнении запроса")


class SWRequester(APIRequester):
    def __init__(self, base_url='https://swapi.dev/api/'):
        self.base_url = base_url

    def get_sw_categories(self) -> list:
        """Возвращает список доступных категорий SWAPI"""
        response = self.get()
        data = response.json()
        return data.keys()

    def get_sw_info(self, sw_type: str) -> str:
        """Возвращает информацию по указанной категории SWAPI"""
        response = self.get(f"/{sw_type}/")
        return response.text


def save_sw_data():
    """Создает директорию data и сохраняет данные по всем категориям SWAPI"""

    os.makedirs("data", exist_ok=True)

    sw_requester = SWRequester()

    try:
        categories = sw_requester.get_sw_categories()
    except Exception as e:
        print(f"Не удалось получить список категорий: {e}")
        return
   
    for category in categories:
        try:
            data = sw_requester.get_sw_info(category)
            
            # Сохраняем в файл с кодировкой UTF-8
            filename = f"data/{category}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            
            print(f"Данные для категории '{category}' сохранены в {filename}")
        except Exception as e:
            print(f"Ошибка при обработке категории {category}: {e}")
