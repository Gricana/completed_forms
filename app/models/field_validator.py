import re
from datetime import datetime
from typing import Type, Literal, TypedDict

FieldType = Literal["date", "phone", "email", "text"]


class ValidatorMap(TypedDict):
    date: Type["FieldValidator"]
    phone: Type["FieldValidator"]
    email: Type["FieldValidator"]
    text: Type["FieldValidator"]


class FieldValidator:
    """
    Базовый валидатор для определения типа поля.
    """

    @staticmethod
    def validate(value: str) -> bool:
        """
        Проверяет, соответствует ли значение конкретному типу.
        Должен быть переопределён в наследниках.
        """
        raise NotImplementedError("Метод `validate` должен быть переопределён")

    @classmethod
    def get_validators(cls) -> ValidatorMap:
        """
        Возвращает словарь доступных валидаторов.
        """
        return {
            "date": DateValidator,
            "phone": PhoneValidator,
            "email": EmailValidator,
            "text": TextValidator,
        }


class DateValidator(FieldValidator):
    formats = ["%d.%m.%Y", "%Y-%m-%d"]

    @staticmethod
    def validate(value: str) -> bool:
        for fmt in DateValidator.formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        return False


class PhoneValidator(FieldValidator):
    @staticmethod
    def validate(value: str) -> bool:
        return bool(re.match(r"^\+?[1-9]\d{0,2} \d{3} \d{3} \d{2} \d{2}$", value))


class EmailValidator(FieldValidator):
    @staticmethod
    def validate(value: str) -> bool:
        return bool(
            re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value)
        )


class TextValidator(FieldValidator):
    @staticmethod
    def validate(value: str) -> bool:
        return bool(re.match(r"^[\w\s.,!?'-]{1,256}$", value))
