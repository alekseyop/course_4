import json
import os
from abc import ABC, abstractmethod

from config import DATA_DIR


class VacancyManager(ABC):
    __slots__ = 'id', 'name', 'area', 'url', 'salary', 'requirements', 'responsibility'

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class VacancyManagerJSON(VacancyManager):
    def __init__(self):
        self.file_full_name = os.path.join(DATA_DIR, 'vacancies.json')
        pass

    def add_vacancy(self, vacancy):
        pass

    def get_vacancies(self, **criteria):
        pass

    def delete_vacancy(self, vacancy_id):
        pass

    def json_saver(self, vacancies):
        """
        Сохранение вакансий в JSON
        :param vacancies:
        :return:
        """
        vacancy_dicts = []
        for vacancy in vacancies:
            vacancy_dict = {
                "id": vacancy.id,
                "name": vacancy.name,
                "area": vacancy.area,
                "url": vacancy.url,
                "salary": vacancy.salary,
                "requirements": vacancy.requirements,
                "responsibility": vacancy.responsibility
            }
            vacancy_dicts.append(vacancy_dict)
        # file_full_name = os.path.join(DATA_DIR, 'vacancies.json')
        with open(self.file_full_name, 'w', encoding='utf-8') as f:
            json.dump(vacancy_dicts, f, ensure_ascii=False, indent=4)
        print(f'Вакансии {len(vacancies)} шт. сохранены в {self.file_full_name}')

    # Заглушки для будущих методов интеграции с базами данных или удаленными хранилищами
    def connect(self):
        pass

    def disconnect(self):
        pass
