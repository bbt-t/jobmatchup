from json import dump, dumps, load, loads, JSONDecodeError

from ..entity.vacancy import VacancyDefault


__all__ = ["JSONSaverFile"]


class JSONSaverFile:
    """
    Class for store in file (json).
    """

    __slots__ = "file_path"

    def __init__(self, file_path: str):
        self.file_path = file_path

    def add_vacancy(self, vacancy: VacancyDefault | list[VacancyDefault, ...]) -> None:
        """
        Save vacancy in file.
        :param vacancy: Vacancy object
        """
        with open(self.file_path, "a+") as f:
            try:
                data = load(f)
            except JSONDecodeError:
                try:
                    dump([vacancy.json(by_alias=True)], f)
                except AttributeError:
                    dump([v.json(by_alias=True) for v in vacancy], f)
            else:
                try:
                    data.append(vacancy.json(by_alias=True))
                except AttributeError:
                    for v in vacancy:
                        data.append(v.json(by_alias=True))
                finally:
                    dump(data, f)

    def get_vacancies_by_salary(self, salary_min: int) -> list:
        """
        Select vacancies by salary.
        :param salary_min: salary
        :return: vacancies objects
        """
        with open(self.file_path) as f:
            data = loads(f.read())

        return [VacancyDefault.parse_obj(vacancy) for vacancy in data if vacancy.get("salary_min") <= salary_min]

    def delete_vacancy(self, vacancy_url: str) -> None:
        """
        Delete vacancy.
        :param vacancy_url: vacancy url
        """
        with open(self.file_path, "x+") as f:
            data: list = loads(f.read())
            for vacancy in data:
                if vacancy.get("url") == vacancy_url:
                    data.remove(vacancy)
            f.write(dumps(data))
