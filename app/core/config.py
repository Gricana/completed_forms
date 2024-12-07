import os
from typing import Dict, Any

from app.core.base import BaseStorageConfig
from app.core.exceptions import StorageConfigError
from app.core.mongodb import MongoDBConfig
from app.core.tinydb import TinyDBConfig


class StorageConfigFactory:
    """
    Фабрика для создания конфигурации хранилища.

    На основе типа хранилища возвращает соответствующий объект конфигурации.
    Если передан неизвестный тип, выбрасывается исключение.
    """

    _config_classes = {
        "MongoDB": MongoDBConfig,
        "TinyDB": TinyDBConfig,
    }

    @classmethod
    def create_config(cls, storage_type: str) -> BaseStorageConfig:
        """
        Создает объект конфигурации для указанного типа хранилища.

        :param storage_type: Тип хранилища (например, "MongoDB" или "TinyDB").
        :return: Объект конфигурации хранилища.
        :raises StorageConfigError: Если передан неизвестный тип хранилища.
        """
        config_class = cls._config_classes.get(storage_type)
        if not config_class:
            raise StorageConfigError(f"Unknown storage type: {storage_type}")
        return config_class()


def get_storage_config() -> Dict[str, Any]:
    """
    Возвращает текущую конфигурацию хранилища на основе переменной окружения.

    :return: Словарь с ключами `STORAGE_TYPE` и `STORAGE_PARAMS`.
    :raises StorageConfigError: Если указанный тип хранилища неизвестен.
    """
    storage_type = os.getenv("STORAGE_TYPE", "TinyDB")
    config = StorageConfigFactory.create_config(storage_type)
    return {"STORAGE_TYPE": storage_type, "STORAGE_PARAMS": config.get_params()}


try:
    CONFIG = get_storage_config()
except StorageConfigError as e:
    print(f"Storage configuration error: {e}")
