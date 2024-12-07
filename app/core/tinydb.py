import os
from typing import Dict, Any

from app.core.base import BaseStorageConfig


class TinyDBConfig(BaseStorageConfig):
    """
    Конфигурация для TinyDB.

    Загружает параметры хранилища из переменных окружения или использует значения по умолчанию:
    - `STORAGE_NAME`: Имя файла базы данных. Значение по умолчанию — "forms.json".
    - `STORAGE_COLLECTION`: Название коллекции. Значение по умолчанию — "forms".
    """

    def __init__(self):
        """
        Инициализирует параметры конфигурации TinyDB.
        """
        self.params: Dict[str, Any] = {
            "NAME": os.getenv("STORAGE_NAME", "forms.json"),
            "COLLECTION": os.getenv("STORAGE_COLLECTION", "forms"),
        }

    def validate(self) -> None:
        """
        Метод валидации конфигурации для TinyDB.

        TinyDB не требует сложной валидации, поэтому метод пуст.
        """
        pass

    def get_params(self) -> Dict[str, Any]:
        """
        Возвращает параметры конфигурации TinyDB.

        :return: Словарь с параметрами `NAME` и `COLLECTION`.
        """
        return self.params
