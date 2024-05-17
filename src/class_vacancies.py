import json
import os
import pandas as pd
import openpyxl
from abc import ABC, abstractmethod
from config import ROOT_DIR
from os import path
from src.class_api import HeadHunterAPI

print(ROOT_DIR)


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
            self.url = args[0].get('alternate_url')

            args[0]['salary']['from'] = args[0]['salary']['from'] if args[0]['salary']['from'] is not None else 0
            args[0]['salary']['to'] = args[0]['salary']['to'] if args[0]['salary']['to'] is not None else 0

            args[0]['salary']['currency'] = args[0]['salary']['currency'] \
                if args[0]['salary']['currency'] != 'RUR' else 'RUB'
            self.salary = args[0].get('salary')

            self.requirements = str(args[0]['snippet']['requirement']).replace(
                "<highlighttext>", "").replace("</highlighttext>", "")

            self.responsibility = str(args[0]['snippet']['responsibility']).replace(
                "<highlighttext>", "").replace("</highlighttext>", "")

    def del_vacancy(self):
        """ Метод для удаления вакансий"""
        try:
            print(self)
        except NameError as e:
            print("Экземпляр класса Vacancy был удален: ", e)
        del self

    def add_vacancy(self, *args):
        """ Метод для добавления вакансий
        :param args: параметры вакансии
        :return:  в виде списка словарей json
        """
        return self.append(args[0])


    def get_vacancies(self, *args):
        """ Метод для получения вакансий
        :param args: параметры для поиска вакансий
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

        Vacancy.json_saver(self, list_vacancies)

        return list_vacancies

    def __repr__(self):
        return (f"{self.__id}, {self.name}, {self.area}, {self.url}, {self.salary},"
                f" {self.requirements}, {self.responsibility}")

    def __str__(self):
        solary = (f"от {self.salary.get('from')} до {self.salary.get('to')}"
                  f" {self.salary.get('currency')} {'грязная' if self.salary.get('gross') else 'чистая'}")
        return (f"id: {self.id}\n"
                f"Название: {self.name}\n"
                f"Регион: {self.area}\n"
                f"Ссылка: {self.url}\n"
                f"Зарплата: {solary}\n"
                f"Требования: {self.requirements}\n"
                f"Обязанности: {self.responsibility}\n")

    def json_saver(self, *args):
        """
        Сохранение вакансий в JSON
        :param args:
        :return:
        """
        vacancy_dicts = []
        for vacancy in args[0]:
            vacancy_dict = {
                "id": vacancy.__id,
                "name": vacancy.name,
                "area": vacancy.area,
                "url": vacancy.url,
                "salary": vacancy.salary,
                "requirements": vacancy.requirements,
                "responsibility": vacancy.responsibility
            }
            vacancy_dicts.append(vacancy_dict)
        file_full_name = os.path.join(ROOT_DIR, 'data', 'vacancies.json')
        with open(file_full_name, 'w', encoding='utf-8') as f:
            json.dump(vacancy_dicts, f, ensure_ascii=False, indent=4)
        print(f'Вакансии {len(args[0])} шт. сохранены в {file_full_name}')

    def sort_vacancies(self, *args):
        """
        Сортировка вакансий по зарплате
        :param args:
        :return:
        """
        # list_vacancies = self.cast_to_object_list(*args)
        list_vacancies_sorted = sorted(args[0], key=lambda x: (x.salary.get('from'), x.salary.get('to')))
        Vacancy.json_saver(self, list_vacancies_sorted)
        return # list_vacancies_sorted

    def sort_vacancies_reversed(self, *args):
        """
        Сортировка вакансий по названию
        :param args:
        :return:
        """
        list_vacancies = self.cast_to_object_list(*args)
        list_vacancies_sorted = sorted(list_vacancies, key=lambda x: (x.salary.get('from'), x.salary.get('to')),
                                       reverse=True)
        return list_vacancies_sorted
