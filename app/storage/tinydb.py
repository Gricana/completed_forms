from typing import List

from app.models.form_template import FormTemplate
from app.storage.base import Storage
from tinydb import TinyDB


class TinyDBStorage(Storage):
    """
    Реализация хранилища на основе TinyDB.
    """

    def __init__(self, NAME: str, COLLECTION: str):
        """
        Инициализация хранилища TinyDB.

        :param NAME: Имя файла базы данных.
        :param COLLECTION: Имя коллекции в базе данных.
        """
        self.db = TinyDB(NAME).table(COLLECTION)

    def get_templates(self) -> List[FormTemplate]:
        """
        Возвращает список всех шаблонов.

        :return: Список объектов `FormTemplate`.
        """
        raw_data = self.db.all()
        return [FormTemplate(**doc) for doc in raw_data]
