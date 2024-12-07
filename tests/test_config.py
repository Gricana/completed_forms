import pytest

from app.core.config import StorageConfigFactory, get_storage_config
from app.core.exceptions import StorageConfigError
from app.core.mongodb import MongoDBConfig
from app.core.tinydb import TinyDBConfig


class MockMongoDBConfig(MongoDBConfig):
    """Мок для MongoDB конфигурации."""

    def get_params(self):
        return {
            "HOST": "mongo",
            "NAME": "form_storage",
            "COLLECTION": "forms",
        }


class MockTinyDBConfig(TinyDBConfig):
    """Мок для TinyDB конфигурации."""

    def get_params(self):
        return {
            "NAME": "forms.json",
            "COLLECTION": "forms",
        }


@pytest.fixture
def mock_storage_configs(monkeypatch):
    """Заменяем реальные классы конфигураций моками."""
    monkeypatch.setattr(
        StorageConfigFactory,
        "_config_classes",
        {"MongoDB": MockMongoDBConfig, "TinyDB": MockTinyDBConfig},
    )


def test_factory_create_mongodb_config(mock_storage_configs):
    """Тест успешного создания MongoDB конфигурации."""
    config = StorageConfigFactory.create_config("MongoDB")
    assert isinstance(config, MockMongoDBConfig)
    assert config.get_params() == {
        "HOST": "mongo",
        "NAME": "form_storage",
        "COLLECTION": "forms",
    }


def test_factory_create_tinydb_config(mock_storage_configs):
    """Тест успешного создания TinyDB конфигурации."""
    config = StorageConfigFactory.create_config("TinyDB")
    assert isinstance(config, MockTinyDBConfig)
    assert config.get_params() == {"NAME": "forms.json", "COLLECTION": "forms"}


def test_factory_invalid_storage_type(mock_storage_configs):
    """Тест обработки неизвестного типа хранилища."""
    with pytest.raises(StorageConfigError, match="Unknown storage type: Redis"):
        StorageConfigFactory.create_config("Redis")


@pytest.mark.parametrize(
    "env_var,expected_config,expected_params",
    [
        (
            "MongoDB",
            MockMongoDBConfig,
            {
                "HOST": "mongo",
                "NAME": "form_storage",
                "COLLECTION": "forms",
            },
        ),
        ("TinyDB", MockTinyDBConfig, {"NAME": "forms.json", "COLLECTION": "forms"}),
    ],
)
def test_get_storage_config(
    monkeypatch, mock_storage_configs, env_var, expected_config, expected_params
):
    """Тест функции get_storage_config с разными значениями STORAGE_TYPE."""
    monkeypatch.setenv("STORAGE_TYPE", env_var)

    config = get_storage_config()
    assert config["STORAGE_TYPE"] == env_var
    assert isinstance(config["STORAGE_PARAMS"], dict)
    assert config["STORAGE_PARAMS"] == expected_params


def test_get_storage_config_default(monkeypatch, mock_storage_configs):
    """Тест get_storage_config с отсутствующей переменной окружения STORAGE_TYPE."""
    monkeypatch.delenv("STORAGE_TYPE", raising=False)

    config = get_storage_config()
    assert config["STORAGE_TYPE"] == "TinyDB"
    assert isinstance(config["STORAGE_PARAMS"], dict)
    assert config["STORAGE_PARAMS"] == {"NAME": "forms.json", "COLLECTION": "forms"}


def test_get_storage_config_invalid_storage_type(monkeypatch, mock_storage_configs):
    """Тест get_storage_config с невалидным STORAGE_TYPE."""
    monkeypatch.setenv("STORAGE_TYPE", "InvalidDB")

    with pytest.raises(StorageConfigError, match="Unknown storage type: InvalidDB"):
        get_storage_config()


def test_factory_with_real_classes(monkeypatch):
    """Тест работы StorageConfigFactory с реальными классами конфигураций."""
    monkeypatch.delenv("STORAGE_TYPE", raising=False)
    config = StorageConfigFactory.create_config("TinyDB")
    assert isinstance(config, TinyDBConfig)
