import logging
from datetime import datetime
from re import sub
from urllib import request, error

from ..entity.hh import HeadHunterAPIVacancies
from ..entity.vacancy import Vacancy

from dateutil.tz import UTC

__all__ = ['HeadHunterAPI']


class HeadHunterAPI:
    """
    Class for working with API HeadHunter.
    """
    def get_vacancies(self, search: str, amt: int | str) -> list[Vacancy, ...]:
        """
        Search query.
        :param amt: how much to get (no more than 100)
        :param search: what we want to find
        :return: received vacancies containing the word (search param) in Vacancy-object
        """
        data_raw: str = self._load_from_url(f"https://api.hh.ru/vacancies?text={search}&per_page={amt}")
        vacancies_items = HeadHunterAPIVacancies.parse_raw(data_raw).items

        return [
            Vacancy(
                title=item.name,
                url=item.alternate_url,
                date_published_timestamp=self._date_to_timestamp(item.published_at),
                city="не указан" if not item.address or not item.address.city else item.address.city,
                requirements=self._requirements_formatter(item),
                salary_min=0 if not item.salary else item.salary.minimal,
                salary_max=0 if not item.salary else item.salary.maximum,
                currency='RUB' if not item.salary else item.salary.currency,
                ) for item in vacancies_items
        ]

    @staticmethod
    def _load_from_url(url: str) -> str | None:
        """
        Load json (from url).
        :param url: URL to upload data
        :return: loaded data from url
        """
        try:
            with request.urlopen(url) as url:
                return url.read().decode()
        except error as e:
            logging.error(f'error :: {repr(e)} ::')

    @staticmethod
    def _requirements_formatter(item) -> str:
        """
        Collection of information.
        :param item: API answer (in dict)
        :return: info
        """
        return f"Опыт: {item.experience.name}\n" \
               f"Тип занятости: {item.employment.name}\n" \
               f"Описание: {sub('<[^<]+?>', '', item.snippet.requirement)}"  # <- remove html

    @staticmethod
    def _date_to_timestamp(date_time: datetime) -> int:
        """
        Parse datetime (UTC) and conversion to timestamp
        :param date_time: string representation of a date
        :return: timestamp
        """
        return int(round(date_time.astimezone(UTC).timestamp()))
