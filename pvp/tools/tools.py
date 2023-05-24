
from pvp.api.vacancy_service import VacancyServiceInterface
# from ..storage.db import VacancySaverInterface
from pvp.entity.vacancy import Vacancy


__all__ = ['search_vacancies']


def search_vacancies(api_object: VacancyServiceInterface, search_query: str) -> list[Vacancy, ...]:
    return api_object.get_vacancies(search_query)


def filter_vacancies(vacancies: list[Vacancy, ...], filter_words: list) -> list[Vacancy, ...]:
    """
    Фильтрация вакансий.
    :param vacancies: полученные вакансии с разных платформы
    :param filter_words: ключевые слова для фильтрации вакансий
    :return:
    """
    return [vacancy for vacancy in vacancies if any([w in vacancy.requirements for w in filter_words])]


def sort_vacancies(filtered_vacancies: list[Vacancy, ...]) -> list[Vacancy, ...]:
    """
    Сортировка отфильтрованных вакансий.
    :param filtered_vacancies: отфильтрованные вакансии
    :return:
    """
    pass


def get_top_vacancies(sorted_vacancies: list[Vacancy, ...], top_n: int) -> list:
    """

    :param sorted_vacancies: отсортированные вакансии
    :param top_n: количество вакансий для вывода в топ
    :return:
    """
    return sorted_vacancies[:top_n]


def show_vacancies(top_vacancies: list[Vacancy, ...]) -> None:
    """
    Вывод результата.
    :param top_vacancies:
    :return:
    """
    for item in top_vacancies:
        print(item)


def test_import_func():
    print('YAHOO!!!')
