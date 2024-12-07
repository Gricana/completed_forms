from typing import Union

from fastapi import FastAPI, Request

from app.api.schema import get_form_schema
from app.models.form_template import FormData, FormTemplate
from app.models.response import TemplateNameResponse, FieldTypeResponse
from app.services.form_service import FormService

app = FastAPI()

service = FormService()


@app.post("/get_form", **get_form_schema)
async def get_form(request: Request) -> Union[TemplateNameResponse, FieldTypeResponse]:
    """
    Обрабатывает данные формы и возвращает результат.

    Эндпоинт принимает данные формы, отправленные в формате
    `application/x-www-form-urlencoded`, передает их в сервис обработки
    и возвращает результат в одном из следующих форматов:
    - Если шаблон найден, возвращается имя шаблона.
    - Если шаблон не найден, возвращается словарь с типами полей.

    :param request: Объект запроса
    :return: Union[TemplateNameResponse, FieldTypeResponse]: Ответ с именем
             шаблона или ответ с типами полей
    """
    data_dict = dict(await request.form())
    form_data = FormData(data=data_dict)
    result = service.process_form(form_data)

    if isinstance(result, FormTemplate):
        return TemplateNameResponse(template_name=result.name)

    return FieldTypeResponse(root=result)
