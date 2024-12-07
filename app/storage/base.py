from typing import List, Protocol

from app.models.form_template import FormTemplate


class Storage(Protocol):
    """
    Интерфейс для работы с хранилищами данных.
    """

    def get_templates(self) -> List[FormTemplate]:
        """
        Получает список всех шаблонов форм.

        :return: Список объектов типа `FormTemplate`.
        """
        pass
