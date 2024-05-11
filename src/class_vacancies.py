from abc import ABC, abstractmethod

from class_api import HeadHunterAPI


class VacancyClass(ABC):
    """ Абстрактный класс для получения вакансий """

    @abstractmethod
    def get_vacancies(self, search_query):
        """ Метод абстрактного класса для получения вакансий """
        pass


class Vacancy(VacancyClass):

    def get_vacancies(self, search_query):
        """ Метод для получения вакансий
        :param search_query: параметры для поиска вакансий
        :return: вакансии в виде списка словарей json
        """
        hh_api = HeadHunterAPI(search_query)
        hh_vacancies = hh_api.get_api_request()
        return hh_vacancies


keyword = 'python'
Vacancy().get_vacancies(keyword)
