import re
from datetime import datetime
from typing import Dict, Literal, Callable, Tuple, List

from pydantic import BaseModel, Field, model_validator

FieldType = Literal["date", "phone", "email", "text"]


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

    Поле:
    - `data`: Словарь, содержащий поля формы и их значения.
    """

    data: Dict[str, str] = Field(..., description="Данные формы")

    @staticmethod
    def _try_parse_date(value: str, date_format: str) -> bool:
        """
        Пробует преобразовать строку в дату по указанному формату.

        :param value: Строка для преобразования.
        :param date_format: Формат, в котором ожидается дата.
        :return: True, если строка соответствует формату даты, иначе False.
        """
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_validators() -> List[Tuple[FieldType, Callable[[str], bool]]]:
        """
        Возвращает список валидаторов для различных типов полей.

        :return: Список валидаторов для каждого типа данных.
        """
        return [
            (
                "date",
                lambda v: any(
                    FormData._try_parse_date(v, fmt) for fmt in ["%d.%m.%Y", "%Y-%m-%d"]
                ),
            ),
            (
                "phone",
                lambda v: bool(
                    re.match(r"^\+?[1-9]\d{0,2} \d{3} \d{3} \d{2} \d{2}$", v)
                ),
            ),
            (
                "email",
                lambda v: bool(
                    re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v)
                ),
            ),
            ("text", lambda v: bool(re.match(r"^[\w\s.,!?'-]{1,256}$", v))),
        ]

    def validate_field(self, value: str) -> FieldType:
        """
        Валидирует значение и определяет его тип.

        :param value: Строка для валидации.
        :return: Тип поля, определённый на основе валидации.
        """
        for field_type, validator in self.get_validators():
            if validator(value):
                return field_type
        return "text"

    def detect_field_types(self) -> Dict[str, FieldType]:
        """
        Выполняет типизацию полей на лету.

        :return: Словарь с типами для каждого поля.
        """
        return {
            field_name: self.validate_field(value)
            for field_name, value in self.data.items()
        }
