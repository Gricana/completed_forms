from app.core.config import CONFIG
from app.storage.base import Storage
from app.storage.registry import StorageRegistry


class StorageFactory:
    """
    Фабрика для создания экземпляра хранилища.
    """

    @staticmethod
    def get_storage() -> Storage:
        """
        Возвращает экземпляр хранилища на основе конфигурации.
        """
        storage_type = CONFIG.get("STORAGE_TYPE", "TinyDB")
        storage_cls = StorageRegistry.get_storage(storage_type)
        return storage_cls(**CONFIG.get("STORAGE_PARAMS", {}))
