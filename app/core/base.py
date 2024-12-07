from typing import Dict, Any


class BaseStorageConfig:
    """
    Базовый класс для конфигураций хранилищ.

    Этот класс предоставляет интерфейс для конфигураций различных хранилищ.
    """

    def validate(self) -> None:
        """
        Проверяет корректность конфигурации.

        Если конфигурация невалидна, ожидается выброс исключения.

        :raises NotImplementedError: если метод не реализован.
        """
        raise NotImplementedError(
            "Метод `validate` должен быть реализован в наследниках."
        )

    def get_params(self) -> Dict[str, Any]:
        """
        Возвращает параметры конфигурации.

        :return: Словарь с параметрами конфигурации.
        :raises NotImplementedError: если метод не реализован.
        """
        raise NotImplementedError(
            "Метод `get_params` должен быть реализован в наследниках."
        )
