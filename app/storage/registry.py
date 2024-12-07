from typing import Dict, Type

from app.storage.base import Storage


class StorageRegistry:
    """
    Реестр хранилищ для динамического выбора реализации.

    Это класс, который управляет регистрацией и выбором различных типов хранилищ.

    Атрибуты:
    - `_registry`: Словарь, где ключами являются имена типов хранилищ,
                   значениями - классы хранилищ.
    """

    _registry: Dict[str, Type[Storage]] = {}

    @classmethod
    def register(cls, name: str, storage_cls: Type[Storage]) -> None:
        """
        Регистрирует класс хранилища с заданным именем.

        :param name: Имя типа хранилища.
        :param storage_cls: Класс хранилища, который будет зарегистрирован.
        """
        cls._registry[name] = storage_cls

    @classmethod
    def get_storage(cls, name: str) -> Type[Storage]:
        """
        Возвращает зарегистрированный класс хранилища по имени.

        :param name: Имя типа хранилища.
        :return: Класс хранилища, зарегистрированный под данным именем.
        :raises ValueError: Если хранилище с таким именем не зарегистрировано.
        """
        if name not in cls._registry:
            raise ValueError(f"Storage type '{name}' is not registered.")
        return cls._registry[name]
