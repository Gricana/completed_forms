import pytest
from app.models.form_template import FormData, FormTemplate


@pytest.fixture
def form_data():
    """
    Фикстура для предоставления данных формы.
    Возвращает объект FormData с полями:
    - email: электронная почта.
    - phone: телефон.
    - message: текст сообщения.
    - date: дата.
    """
    return FormData(
        data={
            "email": "test@example.com",
            "phone": "+1 123 456 78 90",
            "message": "Hello, this is a test message",
            "date": "2023-12-06",
        }
    )


@pytest.fixture
def form_template():
    """
    Фикстура для предоставления корректного шаблона формы.
    Возвращает словарь с полями:
    - name: имя шаблона.
    - email, phone, message: типы полей.
    """
    return {
        "name": "Contact Form",
        "email": "email",
        "phone": "phone",
        "message": "text",
    }


@pytest.fixture
def invalid_form_template():
    """
    Фикстура для предоставления некорректного шаблона формы.
    Шаблон не содержит обязательного поля `name`.
    """
    return {"email": "email", "phone": "phone", "message": "text"}


def test_validate_field_email(form_data):
    """
    Проверяет, что метод validate_field корректно определяет тип `email`.
    """
    assert form_data.validate_field("test@example.com") == "email"


def test_validate_field_phone(form_data):
    """
    Проверяет, что метод validate_field корректно определяет тип `phone`.
    """
    assert form_data.validate_field("+7 123 456 78 90") == "phone"


def test_validate_field_date(form_data):
    """
    Проверяет, что метод validate_field распознает дату в различных форматах.
    """
    assert form_data.validate_field("2023-12-06") == "date"
    assert form_data.validate_field("06.12.2023") == "date"


def test_validate_field_text(form_data):
    """
    Проверяет, что метод validate_field корректно определяет текстовые поля.
    """
    assert form_data.validate_field("Hello, world!") == "text"


def test_detect_field_types(form_data):
    """
    Проверяет, что метод detect_field_types возвращает правильные типы полей.
    Ожидаемый результат: словарь с типами всех полей формы.
    """
    expected = {"email": "email", "phone": "phone", "message": "text", "date": "date"}
    assert form_data.detect_field_types() == expected


def test_split_name_and_fields(form_template):
    """
    Проверяет, что модель FormTemplate корректно разбивает шаблон на `name` и `fields`.
    """
    template = FormTemplate(**form_template)
    assert template.name == "Contact Form"
    assert template.fields == {"email": "email", "phone": "phone", "message": "text"}


def test_split_invalid_fields(invalid_form_template):
    """
    Проверяет, что при отсутствии обязательного поля `name` выбрасывается ValueError.
    """
    with pytest.raises(ValueError, match="Поле `name` обязательно для шаблона формы"):
        FormTemplate(**invalid_form_template)


def test_get_field_types(form_template):
    """
    Проверяет, что метод get_field_types возвращает правильные типы полей шаблона.
    """
    template = FormTemplate(**form_template)
    assert template.get_field_types() == {
        "email": "email",
        "phone": "phone",
        "message": "text",
    }
