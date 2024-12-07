from typing import Union

from app.models.response import TemplateNameResponse, FieldTypeResponse

#: Метаданные для эндпоинта `/get_form`
get_form_schema = {
    "response_model": Union[TemplateNameResponse, FieldTypeResponse],
    "summary": "Обработка формы",
    "description": (
        "Этот эндпоинт принимает данные формы (поля и их значения) и выполняет обработку. "
        "\nЕсли данные соответствуют шаблону формы, возвращается имя шаблона. "
        "\nВ противном случае возвращаются типы переданных полей."
    ),
    "openapi_extra": {
        "requestBody": {
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                    },
                    "example": {
                        "email": "example@example.com",
                        "phone": "+7 999 456 78 90",
                        "message": "Hello world!",
                    },
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Успешная обработка формы",
            "content": {
                "application/json": {
                    "examples": {
                        "template_found": {
                            "summary": "Шаблон найден",
                            "value": {"template_name": "Contact Form"},
                        },
                        "template_not_found": {
                            "summary": "Шаблон не найден",
                            "value": {"email": "email", "phone": "phone"},
                        },
                    },
                }
            },
        },
    },
}
