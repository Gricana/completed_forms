## Описание проекта
Form Service — это сервис для автоматического определения и обработки форм. 
Сервис анализирует данные формы, сопоставляет их с заранее заданными шаблонами и возвращает либо имя подходящего шаблона, либо структуру типов полей, если шаблон не найден.

## Основной функционал
- **Обработка данных формы**: автоматическое определение типа данных в полях формы.
- **Сопоставление шаблонов:** поиск подходящего шаблона формы из хранилища.
- **Возврат структуры полей:** если шаблон не найден, возвращается структура типов полей формы.
- **Гибкость хранилищ:** поддержка работы с несколькими хранилищами, такими как:
	- _MongoDB_
	- _TinyDB_

## Технологический стек
- Язык: Python 3.12
- Веб-фреймворк: FastAPI
- Хранилище данных: MongoDB, TinyDB
- Тестирование: pytest
- Управление зависимостями: Poetry
- Контейнеризация: Docker, Docker Compose

## Установка и запуск

### Настройка проекта
1. Склонируйте репозиторий:
```bash
git clone https://github.com/Gricana/completed_forms
cd completed_forms
```

2. Перейдите в файл [.env](https://github.com/Gricana/completed_forms/blob/main/.env) для указания переменных окружения (пример 
   конфигурации):

- Конфигурация для Mongo:
```bash
STORAGE_TYPE=MongoDB
STORAGE_HOST=mongo
STORAGE_NAME=form_storage
STORAGE_COLLECTION=forms
```

- Конфигурация для TinyDB:
```bash
STORAGE_TYPE=TinyDB
STORAGE_NAME=data/forms.json
STORAGE_COLLECTION=forms
```

### Запуск проекта

- Запуск контейнеров:
```bash 
docker-compose up -d
```
Приложение будет доступно по адресу: http://localhost:8000/get_form

Документация API: http://localhost:8000/docs

### Тестирование
Для запуска полного пула тестов из Docker используйте:

```bash
docker exec -it completed_forms-app-1 poetry run pytest tests --disable-warnings
```
Для запуска тестовых запросов API из Docker используйте:

```bash
docker exec -it completed_forms-app-1 poetry run pytest -k "test_api" --disable-warnings
```

## Структура проекта
```markdown
.
├── app
│   ├── api
│   │   ├── endpoints.py
│   │   └── schema.py
│   ├── core
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── mongodb.py
│   │   └── tinydb.py
│   ├── models
│   │   ├── form_template.py
│   │   └── response.py
│   ├── services
│   │   └── form_service.py
│   └── storage
│       ├── base.py
│       ├── factory.py
│       ├── mongodb.py
│       ├── registry.py
│       └── tinydb.py
├── data
│   ├── forms.json
│   └── forms_mongo.json
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── poetry.lock
├── pyproject.toml
├── README.md
├── test_endpoints.http
└── tests
    ├── test_api.py
    ├── test_config.py
    ├── test_models.py
    └── test_services.py
```