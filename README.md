# Petstore API Test Framework

Проект автотестов для REST API сервиса [Petstore](https://petstore.swagger.io).

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.14 | Язык |
| pytest | Test runner |
| requests | HTTP client |
| pydantic | Валидация ответов через схемы |
| faker | Генерация тестовых данных |
| allure | Отчёты о запусках |

## Project Structure

```
pytest-api-test-framework/
├── api/
│   ├── api_client.py       # Базовый HTTP клиент (retry, timeout)
│   ├── pet_api.py          # Pet эндпоинты
│   └── user_api.py         # User эндпоинты
├── config/
│   ├── settings.py         # URL окружений, конфигурация
│   └── payloads.py         # Генераторы тестовых данных
├── models/
│   ├── pet_model.py        # Pydantic схема питомца
│   └── user_model.py       # Pydantic схема пользователя
├── tests/
│   ├── api/                # Happy path CRUD тесты
│   ├── negative/           # Негативные сценарии
│   ├── smoke/              # Базовые проверки доступности API
│   └── regression/         # Тесты на найденные баги
├── conftest.py             # Фикстуры (клиенты, фабрики, cleanup)
├── pytest.ini
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/horseheadnebula/pytest-api-test-framework.git
cd pytest-api-test-framework

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

По умолчанию тесты запускаются против `dev` окружения.
Переключить окружение через переменную среды `ENV`:

```bash
ENV=stage pytest
ENV=prod pytest
```

Базовые URL настраиваются в `config/settings.py`.

## Running Tests

```bash
# Все тесты
pytest

# По маркеру
pytest -m smoke
pytest -m api
pytest -m negative

# Конкретный файл
pytest tests/api/test_pet_api.py

# С подробным выводом
pytest -v
```

## Allure Report

```bash
# Запуск с генерацией результатов
pytest --alluredir=allure-results

# Открыть отчёт в браузере
allure serve allure-results
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Минимальные проверки: API живёт и отвечает |
| `api` | Happy path: основные CRUD операции |
| `negative` | Негативные сценарии: невалидные данные, несуществующие ресурсы |
| `regression` | Тесты на конкретные зафиксированные баги |
| `xfail` | Известные баги на стороне API — ожидаемые падения |
