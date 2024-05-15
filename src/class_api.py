from abc import ABC, abstractmethod

import requests


class ClassAPI(ABC):
    """Абстрактный класс API"""

    @abstractmethod
    def get_api_request(self, *args):
        """Метод абстрактного класса для получения запроса к API"""
        pass


class HeadHunterAPI(ClassAPI):
    """Класс для получения API запроса к HeadHunter"""

    def __init__(self, *args):
        """
        Метод инициализации
        :param args: параметры для поиска вакансий
        """
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            "text": args[0],
            "area": 113,
            "only_with_salary": True,
            "page": 0,
            "per_page": 100  # Количество вакансий на страницу
        }

    def get_api_request(self, *args):
        """ Метод класса HeadHunterAPI для
        получения API запроса к HeadHunter
        о вакансиях
        :return: json результат API запроса к HeadHunter"""

        vacancies = []
        page = args[1]//100 + 1
        # page = 20  # Количество страниц
        while self.params.get('page') != page:
            response = requests.get(self.url, headers=self.headers, params=self.params)

            if response.status_code == 200:
                vacancies_data = response.json()['items']
                vacancies.extend(vacancies_data)
                self.params['page'] += 1
                print(f'\rЗагружено: {draw_progress_bar(self.params['page'], page)} ', end='')

            else:
                print("Ошибка при запросе вакансий:", response.status_code)
                break

        print('Всего вакансий:', len(vacancies[:args[1]]))
        return vacancies[:args[1]]

    def __str__(self):
        q = self.url + '?' + '&'.join([f'{key}={value}' for key, value in self.params.items()])
        return q

    def __repr__(self):
        return f"{self.url}?{'&'.join(f'{key}={value}' for key, value in self.params.items())}"


class CurrencyExchangeAPI(ClassAPI):
    """ Класс для получения API запроса к API Центробанка"""

    def get_api_request(self: str, *args):
        """ Метод класса CurrencyExchangeAPI для
        получения API запроса к API Центробанка
        о курсе валюты
        :return: результат API запроса к API Центробанка"""

        # def get_currency_exchange_rate(base_currency, target_currency):
        url = f"https://api.exchangerate-api.com/v4/latest/{self}"
        response = requests.get(url)
        data = response.json()
        rates = data["rates"]
        return rates


def draw_progress_bar(current: int, total: int, bar_length: int=30):
    progress = current / total
    num_ticks = int(bar_length * progress)
    bar = '[' + '#' * num_ticks + '_' * (bar_length - num_ticks) + ']'
    percentage = int(progress * 100)
    return f'{bar} {percentage}%'
