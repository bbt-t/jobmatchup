from dataclasses import dataclass, field
from typing import runtime_checkable, Protocol

from .file_db import JSONSaverFile
from .sql_db import DBSaverSQLite, new_sqlite_db_conn
from ..entity import Vacancy, FileConfig, SQLiteConfig, PGConfig


__all__ = ['Repository']


@runtime_checkable
class VacancySaverInterface(Protocol):
    """
    Saving data interface.
    """
    def add_vacancy(self, vacancy: Vacancy) -> None:
        ...

    def get_vacancies_by_salary(self, salary_min: int) -> list:
        ...

    def delete_vacancy(self, vacancy_url: str) -> None:
        ...


@dataclass
class Repository:
    """
    DataBase repository.
    """
    db: VacancySaverInterface = field(init=False)
    cfg: FileConfig | SQLiteConfig | PGConfig

    def __post_init__(self) -> None:
        self._validate()
        self._db_selection()

    def _validate(self):
        """
        Interface conformance check.
        """
        if isinstance(self.db, VacancySaverInterface):
            raise TypeError("Doesn't match the interface")

    def _db_selection(self) -> None:
        """
        Select db.
        """
        match self.cfg:
            case FileConfig():
                self.db = JSONSaverFile(self.cfg.file_path)
            case SQLiteConfig():
                self.db = DBSaverSQLite(new_sqlite_db_conn(self.cfg.mem, self.cfg.path))
            case PGConfig():
                pass
            case _:
                raise TypeError('Unknown config')
