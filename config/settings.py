import os

ENV = os.getenv("ENV", "dev")

# Просто пример мультиокружения. Увы, данный демо-апи не имеет такой возможности.
BASE_URLS = {
    "dev": "https://petstore.swagger.io/v2",
    "stage": "https://petstore.swagger.io/v2",
    "prod": "https://petstore.swagger.io/v2",
}

BASE_URL = BASE_URLS[ENV]
