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


def test_auto_detect_field_types(form_data):
    """
    Проверяет, что `field_types` автоматически заполняется корректно.
    Ожидаемый результат: словарь с типами всех полей формы.
    """
    expected = {"email": "email", "phone": "phone", "message": "text", "date": "date"}
    assert form_data.field_types == expected


def test_field_validators():
    """
    Проверяет, что валидаторы работают корректно для различных типов.
    """
    from app.models.form_template import FieldValidator

    validators = FieldValidator.get_validators()

    assert validators["email"].validate("test@example.com")
    assert validators["phone"].validate("+1 123 456 78 90")
    assert validators["date"].validate("2023-12-06")
    assert validators["date"].validate("06.12.2023")
    assert not validators["email"].validate("test@examplecom")
    assert not validators["phone"].validate("12345")
    assert not validators["date"].validate("2024/11/09")


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
