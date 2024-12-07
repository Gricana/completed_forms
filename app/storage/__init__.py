from app.storage.mongodb import MongoDBStorage
from app.storage.registry import StorageRegistry
from app.storage.tinydb import TinyDBStorage

# Регистрация хранилищ
StorageRegistry.register("TinyDB", TinyDBStorage)
StorageRegistry.register("MongoDB", MongoDBStorage)
