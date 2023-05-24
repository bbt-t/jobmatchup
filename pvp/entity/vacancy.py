from datetime import datetime, timezone, date
from json import loads as json_loads
from typing import Any, Optional
from urllib import request

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
    default_currency: str = 'RUB'

    def make_dict(self) -> dict:
        """
        Data to dict.
        """
        return dict(
            zip(
                (
                    'title',
                    'url',
                    'date_published',
                    'city',
                    'requirements',
                    'salary_min',
                    'salary_max',
                    'currency'
                ),
                (
                    self.title,
                    self.url.lower(),
                    self.date_published_timestamp,
                    self.city,
                    self.requirements,
                    self.salary_min,
                    self.salary_max,
                    self.currency
                ),
            )
        )

    def currency_exchange_salary_min(self) -> int | None:
        with request.urlopen(f"https://open.er-api.com/v6/latest/{self.currency}") as url:
            data = json_loads(url.read().decode())

        if data["result"] == "success":
            return data["rates"][self.default_currency] * self.salary_min

    def make_date_obj(self) -> date:
        """
        Human-readable date.
        :return: date object
        """
        return datetime.fromtimestamp(self.date_published_timestamp, tz=timezone.utc).date()

    @staticmethod
    def __verify_class(other: Any):
        if not isinstance(other, Vacancy):
            raise TypeError("should be Vacancy object")

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
