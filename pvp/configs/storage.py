from dataclasses import dataclass, field
from typing import Literal
from pathlib import Path

from pvp.entity.db import FileConfig, SQLiteConfig, PGConfig


__all__ = ['DBConfig']


@dataclass
class DBConfig:
    cfg_path: dict[Literal['pg', 'sqlite'], str]

    file: FileConfig = field(repr=False, init=False)

    sqlite: SQLiteConfig = field(repr=False, init=False)
    pg: PGConfig = field(repr=False, init=False)

    def __post_init__(self):
        self._validate_cfg_path()

    def _load_file_cfg(self):
        pass

    def _load_pg_cfg(self):
        pass

    def _load_sqlite_cfg(self):
        pass

    def _validate_cfg_path(self):
        """
        Validate attrs.
        """
        if not isinstance(self.cfg_path, str):
            raise TypeError("param :: data_dir :: should be string")

        if not Path(self.cfg_path).exists():
            raise FileNotFoundError("path not found")
