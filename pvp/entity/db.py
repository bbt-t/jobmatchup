from pydantic import BaseModel


__all__ = ['FileConfig', 'SQLiteConfig']


class FileConfig(BaseModel):
    file_path: str


class SQLiteConfig(BaseModel):
    path: str
    mem: bool = True
