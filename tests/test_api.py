import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_form_valid_template_found():
    """
    Тестирует эндпоинт `/get_form` с данными, соответствующими существующему шаблону.

    Ожидаемый результат:
    - Статус ответа: 200.
    - Тело ответа: Имя найденного шаблона формы.
    """
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/get_form",
            data={
                "email": "test@example.com",
                "phone": "+1 123 456 78 90",
                "message": "Hello",
            },
        )
    assert response.status_code == 200
    assert response.json() == {"template_name": "Contact Form"}


@pytest.mark.asyncio
async def test_get_form_no_template_found():
    """
    Тестирует эндпоинт `/get_form` с данными, которые не соответствуют ни одному шаблону.

    Ожидаемый результат:
    - Статус ответа: 200.
    - Тело ответа: Словарь с типами полей, определенными на основе переданных данных.
    """
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/get_form",
            data={"email": "unknown@example.com", "phone": "+1 123 456 78 90"},
        )
    assert response.status_code == 200
    assert response.json() == {"email": "email", "phone": "phone"}


@pytest.mark.asyncio
async def test_get_form_invalid_request():
    """
    Тестирует эндпоинт `/get_form` с некорректными данными.

    Ожидаемый результат:
    - Статус ответа: 200.
    - Тело ответа: Словарь с типом "text" для неизвестных полей.
    """
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/get_form", data={"unknown_field": "value"})
    assert response.status_code == 200
    assert response.json() == {"unknown_field": "text"}
