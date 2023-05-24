from pydantic import BaseModel


__all__ = ['FileConfig', 'SQLiteConfig', 'PGConfig']


class FileConfig(BaseModel):
    file_path: str


class SQLiteConfig(BaseModel):
    path: str
    mem: bool = True


class PGConfig(BaseModel):
    pass

