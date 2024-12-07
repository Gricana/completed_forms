from typing import Dict, Union, List

from app.models.form_template import FieldType
from app.models.form_template import FormData, FormTemplate
from app.storage.base import Storage
from app.storage.factory import StorageFactory


class FormService:
    """
    Сервис для обработки данных форм и подбора подходящих шаблонов.

    Атрибуты:
    - `storage`: Хранилище данных шаблонов.
    """

    def __init__(self):
        self.storage: Storage = StorageFactory.get_storage()

    def process_form(
        self, form_data: FormData
    ) -> Union[FormTemplate, Dict[str, FieldType]]:
        """
        Универсальный метод для обработки формы:
        - Возвращает имя подходящего шаблона, если он найден.
        - Возвращает словарь с типами полей, если шаблон не найден.

        :param form_data: Данные формы, которые нужно обработать.
        :return: Если шаблон найден, возвращается объект FormTemplate.
                 В противном случае возвращается словарь с типами полей.
        """
        templates = self.storage.get_templates()
        return FormService.match_template(form_data, templates)

    @staticmethod
    def match_template(
        form_data: FormData, templates: List[FormTemplate]
    ) -> Union[FormTemplate, Dict[str, FieldType]]:
        """
        Подбирает подходящий шаблон из списка.
        Если подходящий шаблон не найден, возвращает типизацию полей.

        :param form_data: Данные формы, которые нужно проверить.
        :param templates: Список доступных шаблонов.
        :return: Если шаблон найден, возвращается объект FormTemplate.
                 В противном случае возвращается типизация полей формы в виде словаря.
        """
        input_field_types = form_data.detect_field_types()

        for template in templates:
            if all(
                field_name in input_field_types
                and input_field_types[field_name] == field_type
                for field_name, field_type in template.fields.items()
            ):
                return template

        return input_field_types
