from abc import ABC, abstractmethod

from src.class_api import HeadHunterAPI


class VacancyClass(ABC):
    """ Абстрактный класс для получения вакансий """

    @abstractmethod
    def get_vacancies(self, *args):
        """ Метод абстрактного класса для получения вакансий """
        pass


class Vacancy(VacancyClass):
    """ Класс для работы с вакансиями """
    __slots__ = 'id', 'name', 'area', 'url', 'salary', 'requirements', 'responsibility'
    id: int  # id вакансии
    name: str  # название вакансии
    area: str  # регион вакансии
    url: str  # url вакансии
    salary: dict  # зарплата вакансии
    requirements: str  # требования вакансии
    responsibility: str  # обязанности вакансии

    def __init__(self, *args):
        if len(args) != 0:
            self.__id = args[0].get('id')
            self.name = args[0].get('name')
            self.area = args[0]['area']['name']
            self.url = args[0].get('url')

            args[0]['salary']['from'] = args[0]['salary']['from'] if args[0]['salary']['from'] is not None else 0
            args[0]['salary']['to'] = args[0]['salary']['to'] if args[0]['salary']['to'] is not None else 0

            args[0]['salary']['currency'] = args[0]['salary']['currency'] \
                if args[0]['salary']['currency'] != 'RUR' else 'RUB'
            self.salary = args[0].get('salary')

            self.requirements = str(args[0]['snippet']['requirement']).replace(
                "<highlighttext>", "").replace("</highlighttext>", "")

            self.responsibility = str(args[0]['snippet']['responsibility']).replace(
                "<highlighttext>", "").replace("</highlighttext>", "")

    def get_vacancies(self, *args):
        """ Метод для получения вакансий
        :param search_query: параметры для поиска вакансий
        :return: вакансии в виде списка словарей json
        """
        hh_api = HeadHunterAPI(*args)
        hh_vacancies = hh_api.get_api_request(*args)
        return hh_vacancies

    def cast_to_object_list(self, *args):
        """
        Преобразование набора данных из JSON HH API в список объектов Vacancy
        :param args:
        :return:
        """
        list_vacancies = []
        for vacancy in args[0]:
            list_vacancies.append(Vacancy(vacancy))

        # for i in list_vacancies:
        #     print(repr(i))
        #     # print(i)
        # list_vacancies_sorted = sorted(list_vacancies, key=lambda x: (x.salary.get('from'), x.salary.get('to')))
        # print('\n')
        # for i in list_vacancies_sorted:
        #     print(repr(i))
        #     # print(i)

    def __repr__(self):
        return (f"{self.__id}, {self.name}, {self.area}, {self.url}, {self.salary},"
                f" {self.requirements}, {self.responsibility}")

    def __str__(self):
        solary = f"от {self.salary.get('from')} до {self.salary.get('to')} {self.salary.get('currency')}"
        return (f"id: {self.__id}\n"
                f"Название: {self.name}\n"
                f"Регион: {self.area}\n"
                f"Ссылка: {self.url}\n"
                f"Зарплата: {solary}\n"
                f"Требования: {self.requirements}\n"
                f"Обязанности: {self.responsibility}\n")

