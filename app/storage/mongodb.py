from typing import List

from pymongo import MongoClient

from app.models.form_template import FormTemplate
from app.storage.base import Storage


class MongoDBStorage(Storage):
    """
    Реализация хранилища на основе MongoDB.
    """

    def __init__(self, HOST: str, NAME: str, COLLECTION: str):
        """
        Инициализация хранилища MongoDB.

        :param HOST: Адрес подключения к MongoDB.
        :param NAME: Имя базы данных.
        :param COLLECTION: Имя коллекции в базе данных.
        """
        self.client = MongoClient(HOST)
        self.collection = self.client[NAME][COLLECTION]

    def get_templates(self) -> List[FormTemplate]:
        """
        Возвращает список всех шаблонов из коллекции.

        :return: Список объектов `FormTemplate`, созданных из записей коллекции.
        """
        templates = self.collection.find({}, {"_id": 0})
        return [FormTemplate(**template) for template in templates]
