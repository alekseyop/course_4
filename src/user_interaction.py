# from src.class_vacancies import Vacancy
from src.class_vacancies import Vacancy

from src.class_api import HeadHunterAPI


def user_interaction():
    print('Программа, которая собирает информацию о вакансиях с платформы hh.ru в России,'
          ' сохраняет её в файл и позволяет удобно работать с ней')
    job_request = input('Введите вакансию(например: Python, Python developer, Back-end developer): ')
    job_request_count = 'a'
    while not job_request_count.isdigit():
        job_request_count = input('Введите количество вакансий(целое положительное число до 2000 иначе выход): ')
    job_request_count = int(job_request_count)
    print()
    if job_request_count < 1 or job_request_count > 2001:
        print('Пока)')
        exit()
    vacancies = Vacancy().get_vacancies(job_request, job_request_count)
    print()
    Vacancy().cast_to_object_list(vacancies)
    # print(vacancies)



def draw_progress_bar(current: int, total: int, bar_length: int=30):
    progress = current / total
    num_ticks = int(bar_length * progress)
    bar = '[' + '#' * num_ticks + '_' * (bar_length - num_ticks) + ']'
    percentage = int(progress * 100)
    return f'{bar} {percentage}%'
