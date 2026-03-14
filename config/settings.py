import os

ENV = os.getenv("ENV", "dev")

BASE_URLS = {
    "dev": "https://petstore.swagger.io/v2",
    "stage": "https://petstore.swagger.io/v2",
    "prod": "https://petstore.swagger.io/v2",
}

BASE_URL = BASE_URLS[ENV]

TIMEOUT = 5
