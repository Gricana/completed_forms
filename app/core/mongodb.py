import os
from typing import Dict, Any

from app.core.base import BaseStorageConfig
from app.core.exceptions import StorageConfigError


class MongoDBConfig(BaseStorageConfig):
    """
    Конфигурация для MongoDB.

    Загружает параметры хранилища из переменных окружения:
    - `STORAGE_HOST`: Хост MongoDB.
    - `STORAGE_NAME`: Имя базы данных.
    - `STORAGE_COLLECTION`: Название коллекции.
    """

    def __init__(self):
        """
        Инициализирует параметры конфигурации MongoDB.
        """
        self.params: Dict[str, Any] = {
            "HOST": os.getenv("STORAGE_HOST"),
            "NAME": os.getenv("STORAGE_NAME"),
            "COLLECTION": os.getenv("STORAGE_COLLECTION"),
        }

    def validate(self) -> None:
        """
        Проверяет, что все параметры конфигурации заполнены.

        :raises StorageConfigError: Если один или несколько параметров отсутствуют.
        """
        if not all(self.params.values()):
            raise StorageConfigError("Incomplete MongoDB configuration.")

    def get_params(self) -> Dict[str, Any]:
        """
        Возвращает параметры конфигурации MongoDB.

        :return: Словарь с параметрами `HOST`, `NAME`, `COLLECTION`.
        :raises StorageConfigError: Если параметры конфигурации не валидны.
        """
        self.validate()
        return self.params
