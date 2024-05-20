import json
import os

import pandas as pd

from config import ROOT_DIR
from src.VacancyManager import VacancyManagerJSON
from src.class_api import CurrencyExchangeAPI
from src.class_vacancies import Vacancy


def user_interaction():
    print('Программа, которая собирает информацию о вакансиях с платформы hh.ru в России,'
          ' сохраняет её в файл и позволяет удобно работать с ней')
    job_request = input('Введите вакансию(например: Python, Python developer, комбайнер): ')
    job_request_count = 'a'
    while not job_request_count.isdigit():
        job_request_count = input('Введите количество вакансий(целое положительное число 0 - 2000 если вне диапазона '
                                  'выход): ')
    job_request_count = int(job_request_count)
    print()
    if job_request_count < 1 or job_request_count > 2001:
        print('Пока)')
        exit()
    vacancies = Vacancy().get_vacancies(job_request, job_request_count)
    print()
    list_vacancies = Vacancy().cast_to_object_list(vacancies)
    VacancyManagerJSON().json_saver(list_vacancies)

    action = '1'
    while action != '0':
        print("\nПри выполнении действий с вакансиями формируется новый json файл.")
        action = input('\n1 - Вывести список вакансий метод __repr__\n'
                       '2 - Вывести вакансии в столбик метод __str__\n'
                       '3 - Вывести вакансии из json файла в таблицу на экран и сохранить в файл .txt\n'
                       '4 - Сохранить вакансии из json файла в файл .XLSX(Excel)\n'
                       '5 - Сортировать вакансии по зарплате по возрастанию\n'
                       '6 - Сортировать вакансии по зарплате по убыванию\n'
                       '7 - Сформировать JSON с вакансиями по ключевым словам\n'
                       '8 - Сформировать JSON с вакансиями по размеру зарплаты\n'
                       '9 - Сменить валюту в вакансиях\n'
                       '10 - Сформировать первоначальный JSON с вакансиями\n'
                       '0 - Выход\n')
        if action == '1':
            print_repr(list_vacancies)
            continue
        elif action == '2':
            print_column(list_vacancies)
            continue
        elif action == '3':
            print_table()
            continue
        elif action == '4':
            create_xlsx()
            continue
        elif action == '5':
            vacancies_sorted = sorted(vacancies, key=lambda x: (x['salary']['from'], x['salary']['to']), reverse=False)
            list_vacancies = Vacancy().cast_to_object_list(vacancies_sorted)
            print('Вакансии отсортированы по зарплате по возрастанию')
            continue
        elif action == '6':
            vacancies_sorted = sorted(vacancies, key=lambda x: (x['salary']['from'], x['salary']['to']), reverse=True)
            list_vacancies = Vacancy().cast_to_object_list(vacancies_sorted)
            print('Вакансии отсортированы по зарплате по убыванию')
            continue
        elif action == '7':
            new_vacancies = filter_vacancies_by_keywords(vacancies)
            list_vacancies = Vacancy().cast_to_object_list(new_vacancies)
            continue
        elif action == '8':
            print("WARNING! Приведите все вакансии к одной валюте(если требуется)")
            new_vacancies = filter_vacancies_by_salary(vacancies)
            list_vacancies = Vacancy().cast_to_object_list(new_vacancies)
            continue
        elif action == '9':
            new_vacancies = currency_converter(vacancies)
            list_vacancies = Vacancy().cast_to_object_list(new_vacancies)
            continue
        elif action == '10':
            vacancies = Vacancy().get_vacancies(job_request, job_request_count)
            list_vacancies = Vacancy().cast_to_object_list(vacancies)
            VacancyManagerJSON().json_saver(list_vacancies)
            continue
        elif action == '0':
            print('Пока)')
            exit()


def print_repr(list_vacancies):
    """
    Вывод списка вакансий
    :param list_vacancies:
    :return:
    """
    for i in list_vacancies:
        print(Vacancy.__repr__(i))


def print_column(list_vacancies):
    """
    Вывод списка вакансий в столбик
    :param list_vacancies:
    :return:
    """
    for i in list_vacancies:
        print(Vacancy.__str__(i))


def print_table():
    """
    Вывод списка вакансий в таблицу и сохранение в файл output.txt
    :param :
    :return:
    """
    file_full_name = os.path.join(ROOT_DIR, 'data', 'vacancies.json')
    with open(file_full_name, 'r', encoding='utf-8') as f:
        data1 = json.load(f)

    data = []
    for item in data1:
        transformed_item = {
            "Название": item["name"],
            "Регион": item["area"],
            "Ссылка": item["url"],
            "Зарплата от ": item["salary"]["from"],
            "до": item["salary"]["to"],
            "валюта": item["salary"]["currency"],
            "Требования": item["requirements"],
            "Обязанности": item["responsibility"]
        }
        data.append(transformed_item)

    # Получаем список всех ключей
    keys = data[0].keys() if data else []
    text_table = ''
    # Определяем ширину каждой колонки
    column_widths = {}
    for key in keys:
        column_widths[key] = max(len(str(item[key])) for item in data) if data else len(key)
        column_widths[key] = max(column_widths[key], len(key))

    # Выводим заголовки таблицы
    # with open("output.txt", "w") as f:
    for key in keys:
        text_table += (f"{key.ljust(column_widths[key])} | ")
    text_table += ('\n')

    # Выводим разделительную строку
    for key in keys:
        text_table += (f"{'-' * column_widths[key]} | ")
    text_table += ("\n")

    # Выводим данные
    for item in data:
        for key in keys:
            text_table += (f"{str(item.get(key, '')).ljust(column_widths[key])} | ")
        text_table += ('\n')

    print(text_table)
    file_full_name = os.path.join(ROOT_DIR, 'data', 'output.txt')
    with open(file_full_name, "w", encoding='utf-8') as f:
        # f.write(text_table)
        print(text_table, file=f)

    print(f'Таблица сохранена в {file_full_name}')


def create_xlsx():
    """
    Сохранение вакансий в файл .XLSX
    :return:
    """
    file_full_name = os.path.join(ROOT_DIR, 'data', 'vacancies.json')
    with open(file_full_name, 'r', encoding='utf-8') as f:
        data1 = json.load(f)

    data = []
    for item in data1:
        transformed_item = {
            "Название": item["name"],
            "Регион": item["area"],
            "Ссылка": item["url"],
            "Зарплата от ": item["salary"]["from"],
            "до": item["salary"]["to"],
            "валюта": item["salary"]["currency"],
            "Требования": item["requirements"],
            "Обязанности": item["responsibility"]
        }
        data.append(transformed_item)

    file_full_name = os.path.join(ROOT_DIR, 'data', 'output.xlsx')
    df = pd.DataFrame(data)
    df.to_excel(file_full_name)
    print(f'Вакансии сохранены в {file_full_name}')


def currency_converter(vacancies):
    """
    Конвертация валюты
    :return:
    """
    rates = CurrencyExchangeAPI.get_api_request('RUB')
    new_vacancies = []
    for i in vacancies:
        if i['salary']['currency'] != 'RUB':
            i['salary']['from'] = round(i['salary']['from'] / rates[i['salary']['currency']], 2)
            i['salary']['to'] = round(i['salary']['to'] / rates[i['salary']['currency']], 2)
            i['salary']['currency'] = 'RUB'
        new_vacancies.append(i)
    rate_list = list(rates.keys())
    currency = input('Выберите валюту(пример: USD, EUR, RUB,CNY, KZT, BYN ): ').upper()
    if currency == 'RUB' or currency == '':
        print('Валюта не выбрана, сделали всё в RUB')
        return new_vacancies
    if currency in rate_list:
        print(f'Курс {currency} = {1 / rates[currency]} RUB')
    else:
        print('Такой валюты нет и не надо, сделали всё в RUB')
        return new_vacancies

    rates = CurrencyExchangeAPI.get_api_request(currency)
    new_vacancies = []
    for i in vacancies:
        if i['salary']['currency'] != currency:
            i['salary']['from'] = round(i['salary']['from'] / rates[i['salary']['currency']], 2)
            i['salary']['to'] = round(i['salary']['to'] / rates[i['salary']['currency']], 2)
            i['salary']['currency'] = currency
        new_vacancies.append(i)
    return new_vacancies


def filter_vacancies_by_salary(vacancies):
    """
    Фильтрация вакансий по зарплате
    :return:
    """
    salary_from = input('Введите минимальную зарплату(число): ')
    salary_to = input('Введите максимальную зарплату(число): ')
    if not salary_from.isdigit() or not salary_to.isdigit():
        print('Минимальная и максимальная зарплата должны быть числами')
        return vacancies
    salary_from = int(salary_from)
    salary_to = int(salary_to)
    if salary_from > salary_to:
        print('Максимальная зарплата должна быть больше минимальной')
        return vacancies
    new_vacancies = []
    for item in vacancies:
        from_vac = item['salary']['from']
        to_vac = item['salary']['to'] if item['salary']['to'] != 0 else 100000000
        if from_vac <= salary_from <= to_vac or to_vac <= salary_to <= to_vac:
            new_vacancies.append(item)

    print(f'Найдено {len(new_vacancies)} вакансий')
    return new_vacancies


def filter_vacancies_by_keywords(vacancies):
    """
    Фильтрация вакансий по ключевым словам
    :param vacancies:
    :return:
    """
    key_word = input('Введите ключевое слово: ')
    key_word_variant = input(f"Выбрать вакансии с ключевым словом '{key_word}' или без: 1 - с, 2 - без: ")
    if key_word_variant == '1':
        new_vacancies = []
        for item in vacancies:
            if item['snippet']['requirement'] is None or item['snippet']['responsibility'] is None:
                continue
            if key_word in item['snippet']['requirement'] or key_word in item['snippet']['responsibility']:
                new_vacancies.append(item)
        return new_vacancies
    if key_word_variant == '2':
        new_vacancies = []
        for item in vacancies:
            if item['snippet']['requirement'] is None or item['snippet']['responsibility'] is None:
                continue
            if key_word not in item['snippet']['requirement'] and key_word not in item['snippet']['responsibility']:
                new_vacancies.append(item)
        return new_vacancies
    print('Такого варианта нет')

    return vacancies


def draw_progress_bar(current: int, total: int, bar_length: int = 30):
    progress = current / total
    num_ticks = int(bar_length * progress)
    bar = '[' + '#' * num_ticks + '_' * (bar_length - num_ticks) + ']'
    percentage = int(progress * 100)
    return f'{bar} {percentage}%'
