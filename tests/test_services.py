from app.models.form_template import FormData, FormTemplate
from app.services.form_service import FormService


class MockStorage:
    """
    Мок-реализация хранилища для тестов.
    Предоставляет два шаблона форм:
    - Contact Form: содержит поля email, phone и message.
    - Feedback Form: содержит поля customer_name, email и feedback.
    """

    def get_templates(self):
        """
        Возвращает список заранее определённых шаблонов форм.
        """
        return [
            FormTemplate(
                **{
                    "name": "Contact Form",
                    "email": "email",
                    "phone": "phone",
                    "message": "text",
                }
            ),
            FormTemplate(
                **{
                    "name": "Feedback Form",
                    "customer_name": "text",
                    "email": "email",
                    "feedback": "text",
                }
            ),
        ]


def test_process_form_match_template(monkeypatch):
    """
    Тестирует, что метод process_form возвращает корректный шаблон при полном совпадении.
    """
    monkeypatch.setattr(
        "app.storage.factory.StorageFactory.get_storage", lambda: MockStorage()
    )
    service = FormService()
    form_data = FormData(
        data={
            "email": "test@example.com",
            "phone": "+1 123 456 78 90",
            "message": "Hello",
        }
    )
    result = service.process_form(form_data)
    assert isinstance(result, FormTemplate)
    assert result.name == "Contact Form"


def test_process_form_no_match(monkeypatch):
    """
    Тестирует, что метод process_form возвращает словарь типов полей, если шаблон не найден.
    """
    monkeypatch.setattr(
        "app.storage.factory.StorageFactory.get_storage", lambda: MockStorage()
    )
    service = FormService()
    form_data = FormData(
        data={"email": "test@example.com", "phone": "+1 123 456 78 90"}
    )
    result = service.process_form(form_data)
    assert isinstance(result, dict)
    assert result == {"email": "email", "phone": "phone"}
