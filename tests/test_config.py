from pvp.configs import DBConfig, Config
from pvp.entity import FileConfig


from pytest import fixture


@fixture
def get_db_config_obj() -> DBConfig:
    """
    Create Item object.
    """
    return DBConfig(file_path="../tests")


@fixture
def get_db_config_obj_default() -> DBConfig:
    """
    Create Item object.
    """
    return DBConfig()


@fixture
def get_cfg_without_auth() -> Config:
    """
    Create Item object.
    """
    return Config(without_auth=True)


def test_db_config_obj_attributes(get_db_config_obj):
    """
    Attrs test.
    """
    assert isinstance(get_db_config_obj.file_path, str)
    assert get_db_config_obj.file_path == "../tests"


def test_db_config_obj_attributes_default(get_db_config_obj_default):
    """
    Attrs test.
    """
    assert isinstance(get_db_config_obj_default.file_path, str)
    assert get_db_config_obj_default.file_path == "vacancies.json"


def test_init_db_config_obj(get_db_config_obj):
    """
    __init__ test.
    """
    assert isinstance(get_db_config_obj.file, FileConfig)


def test_init_cfg_without_auth(get_cfg_without_auth):
    """
    __init__ test.
    """
    assert get_cfg_without_auth.without_auth is True
    assert get_cfg_without_auth.login_pass_auth is False
    assert get_cfg_without_auth.from_env is False
    assert get_cfg_without_auth.from_json is False


def test_init_hasattr_cfg_without_auth(get_cfg_without_auth):
    assert hasattr(get_cfg_without_auth, "from_toml") is True
    assert hasattr(get_cfg_without_auth, "auth_info") is False
    assert hasattr(get_cfg_without_auth, "app_info") is False
    assert hasattr(get_cfg_without_auth, "token_info") is False
