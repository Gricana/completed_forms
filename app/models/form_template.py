from typing import Dict

from pydantic import BaseModel, Field, model_validator

from app.models.field_validator import FieldType
from app.models.field_validator import FieldValidator


class FormTemplate(BaseModel):
    """
    Шаблон формы, включающий имя и поля с их типами.

    Поля:
    - `name`: Имя шаблона формы.
    - `fields`: Словарь, где ключи — имена полей, а значения — типы этих полей.
    """

    name: str = Field(..., description="Имя шаблона формы")
    fields: Dict[str, FieldType] = Field(
        default_factory=dict, description="Список полей с их типами"
    )

    @model_validator(mode="before")
    @classmethod
    def split_name_and_fields(cls, values) -> Dict[str, any]:
        """
        Извлекает `name` из структуры и оставляет остальные элементы как поля.

        :param values: Исходные данные для шаблона формы.
        :raises ValueError: Если поле `name` отсутствует.
        :raises TypeError: Если данные не являются словарем.
        :return: Словарь с `name` и полями.
        """
        if isinstance(values, dict):
            name = values.pop("name", None)
            if not name:
                raise ValueError("Поле `name` обязательно для шаблона формы")
            fields = {key: value for key, value in values.items()}
            return {"name": name, "fields": fields}
        else:
            raise TypeError("Входные данные должны быть словарем")

    def get_field_types(self) -> Dict[str, FieldType]:
        """
        Возвращает только поля и их типы.

        :return: Словарь с полями и их типами.
        """
        return self.fields


class FormData(BaseModel):
    """
    Данные формы, переданные пользователем.

    Поля:
    - `data`: Словарь, содержащий поля формы и их значения.
    - `field_types`: Словарь, автоматически определяемый на основе значений `data`.
    """

    data: Dict[str, str] = Field(..., description="Данные формы")
    field_types: Dict[str, FieldType] = Field(
        default_factory=dict, description="Типы полей"
    )

    @model_validator(mode="before")
    @classmethod
    def auto_detect_field_types(cls, values: Dict) -> Dict:
        """
        Автоматически определяет типы полей на основе переданных данных.
        """
        data = values.get("data", {})
        validators = FieldValidator.get_validators()

        def detect_type(value: str) -> FieldType:
            for field_type, validator_cls in validators.items():
                if validator_cls.validate(value):
                    return field_type
            return "text"

        values["field_types"] = {
            field: detect_type(value) for field, value in data.items()
        }
        return values
