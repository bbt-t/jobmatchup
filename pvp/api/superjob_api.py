from json import loads as json_loads
from datetime import datetime, timezone, timedelta
from urllib import request

from ..entity.super_job import SuperJobAPIVacancies
from ..entity.vacancy import Vacancy
from ..entity.api import AppInfo, TokenInfo


__all__ = ['SuperJobAPI']


class SuperJobAPI:
    """
    Class for working with API SuperJob.
    """
    _host = 'https://api.superjob.ru/2.0'
    _url_refresh_token = '{}/oauth2/refresh_token/?refresh_token={}&client_id={}&client_secret={}'
    _url_search_vacancies = '{}/vacancies?keyword={}&count={}'

    def __init__(self, app_info: AppInfo, token_info_info: TokenInfo):
        self._app_id, self._secret_key = app_info.dict().values()
        self._token, self._refresh_token, self.expires_in = token_info_info.dict().values()

        self.time_to_refresh_token = datetime.now(tz=timezone.utc) + timedelta(seconds=self.expires_in)

    def _refresh_token(self) -> dict[str, str | int]:
        """
        Refreshing a rotten token.
        :return: new token, refresh token and expire time (sec)
        """
        url = self._url_refresh_token.format(self._host, self._refresh_token, self._app_id, self._secret_key)
        with request.urlopen(url) as url:
            data = json_loads(url.read().decode())
        return data

    def _set_new_values(self):
        data: dict[str, str | int] = self._refresh_token()
        refreshed_valid = TokenInfo(
                token=data['access_token'],
                refresh_token=data['refresh_token'],
                expires_in=data['expires_in'],
        )
        self._token, self._refresh_token, self.expires_in = refreshed_valid.dict().values()

    def get_vacancies(self, search: str, amt: int | str) -> list[Vacancy, ...]:
        """
        Search query.
        :param amt: how much to get (no more than 100)
        :param search: what we want to find
        :return: received vacancies containing the word (search param) in Vacancy-object
        """
        data: str = self._load_from_url(search, amt)
        vacancies_items = SuperJobAPIVacancies.parse_raw(data).objects

        return [
            Vacancy().parse_obj({
                'title': item.profession,
                'url': item.link,
                'date_published_timestamp': item.date_published,
                'city': item.town.title,
                'requirements': self._requirements_formatter(item),
                'salary_min': item.salary_minimal,
                'salary_max': item.salary_maximum,
                'currency': item.currency,
            }) for item in vacancies_items
        ]

    def _load_from_url(self, search: str, amt: int) -> str:
        """
        Load json (from url).
        :param amt: how much to get (no more than 100)
        :param search: what we want to find
        :return: loaded data
        """
        if self.time_to_refresh_token.minute < 5:
            self._set_new_values()

        url = self._url_search_vacancies.format(self._host, search, amt)
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Api-App-Id": self._secret_key,
            "Authorization": f"Bearer {self._token}"
        }

        with request.urlopen(request.Request(url=url, headers=header)) as url:
            data = url.read().decode()
        return data

    @staticmethod
    def _requirements_formatter(item):
        """
        Collection of information.
        :param item: API answer (in dict)
        :return: info
        """
        return f"Опыт: {item.experience.title}\n" \
               f"Тип занятости: {item.type_of_work.title}" \
               f"Описание: {item.candidat}"