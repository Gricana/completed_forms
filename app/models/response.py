from typing import Dict

from pydantic import BaseModel, RootModel

from app.models.form_template import FieldType


class TemplateNameResponse(BaseModel):
    """
    Ответ с именем шаблона формы.

    Поля:
    - `template_name`: Имя шаблона формы.
    """

    template_name: str


class FieldTypeResponse(RootModel):
    """
    Ответ с типами полей формы.

    Поля:
    - `root`: Словарь с именами полей и их типами.
    """

    root: Dict[str, FieldType]
