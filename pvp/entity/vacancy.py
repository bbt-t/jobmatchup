import logging
from datetime import datetime, timezone, date
from json import loads as json_loads
from typing import Any, Optional, LiteralString
from urllib import request, error

from pydantic import BaseModel, AnyHttpUrl


__all__ = ['Vacancy']


class Vacancy(BaseModel):
    """
    Class Vacancy
    """
    title: str | None
    url: AnyHttpUrl | None
    date_published_timestamp: int | None
    city: str | None
    requirements: str | None
    salary_min: Optional[int]
    salary_max: Optional[int]
    currency: str = 'RUB'
    _default_currency: str = 'RUB'

    @property
    def default_currency(self):
        return self._default_currency

    @default_currency.setter
    def default_currency(self, currency: LiteralString):
        self._default_currency = currency

    def currency_exchange_salary_min(self) -> int | None:
        try:
            with request.urlopen(f"https://open.er-api.com/v6/latest/{self.currency}") as url:
                data = json_loads(url.read().decode())

            if data["result"] == "success":
                return data["rates"][self.default_currency] * self.salary_min
        except error as e:
            logging.warning(f'error :: {repr(e)} ::')
            print(f'! {self.currency} not supported !')
        except KeyError as e:
            logging.error(f'error :: {repr(e)} ::')

    def make_date_obj(self) -> date:
        """
        Human-readable date.
        :return: date object
        """
        return datetime.fromtimestamp(self.date_published_timestamp, tz=timezone.utc).date()

    @staticmethod
    def __verify_class(other: Any):
        if not hasattr(other, "salary_min"):
            raise NotImplemented("! should be implemented 'salary_min' attr !")

    def __repr__(self):
        return f"Вакансия {self.title}:\n" \
               f"{self.url}\n" \
               f"{self.make_date_obj()}\n" \
               f"{self.city}\n" \
               f"{self.requirements}\n" \
               f"{self.salary_min} - {self.salary_max} {self.currency}\n"

    def __eq__(self, other):
        self.__verify_class(other)
        return self.salary_min == other.salary_min

    def __ne__(self, other):
        self.__verify_class(other)
        return self.salary_min != other.salary_min

    def __lt__(self, other):
        self.__verify_class(other)
        return self.salary_min < other.salary_min

    def __le__(self, other):
        self.__verify_class(other)
        return self.salary_min <= other.salary_min

    def __gt__(self, other):
        self.__verify_class(other)
        return self.salary_min > other.salary_min

    def __ge__(self, other):
        self.__verify_class(other)
        return self.salary_min >= other.salary_min
