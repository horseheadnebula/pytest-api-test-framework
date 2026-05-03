import random

from faker import Faker

from models.pet_model import Category, PetSchema, Tags
from models.user_model import UserSchema


class GeneratePet:
    _fake = Faker()

    def __init__(
        self,
        pet_id: int | None = None,
        name: str | None = None,
        status: str | None = None,
        category: Category | None = None,
        photo_urls: list[str] | None = None,
        tags: list[Tags] | None = None,
    ):
        # В атрибуты объекта сохраняем переданные аргументы, если ничего не передали то генерируются рандомные данные.
        self.pet_id = random.randint(1000, 9999) if pet_id is None else pet_id
        self.name = GeneratePet._fake.first_name() if name is None else name
        self.status = (
            random.choice(["available", "pending", "sold"])
            if status is None
            else status
        )
        self.category = self._generate_category() if category is None else category
        self.photo_urls = (
            self._generate_photo_urls() if photo_urls is None else photo_urls
        )
        self.tags = self._generate_tags() if tags is None else tags

    @staticmethod
    def _generate_category() -> Category:
        return Category(
            id=random.randint(1, 4), name=random.choice(["dog", "cat", "bird", "fish"])
        )

    @staticmethod
    def _generate_photo_urls() -> list[str]:
        return [GeneratePet._fake.image_url() for _ in range(random.randint(1, 3))]

    @staticmethod
    def _generate_tags() -> list[Tags]:
        return [
            Tags(
                id=random.randint(1, 4),
                name=random.choice(["cute", "angry", "fast", "lazy"]),
            )
        ]

    # Создаём pydentic модель PetSchema, передав данные из атрибутов объекта.
    def build(self) -> PetSchema:
        return PetSchema(
            id=self.pet_id,
            name=self.name,
            status=self.status,
            category=self.category,
            photo_urls=self.photo_urls,
            tags=self.tags,
        )

    # Собераем PetSchema, конвертируем в словарь, поля со значением None выкидываем.
    def build_payload(self) -> dict:
        return self.build().model_dump(exclude_none=True)


class GenerateUser:
    _fake = Faker()

    def __init__(
        self,
        user_id: int | None = None,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        phone: str | None = None,
        user_status: int | None = None,
    ):
        # В атрибуты объекта сохраняем переданные аргументы, если ничего не передали то генерируются рандомные данные.
        self.user_id = random.randint(1000, 9999) if user_id is None else user_id
        self.username = GenerateUser._fake.user_name() if username is None else username
        self.first_name = (
            GenerateUser._fake.first_name() if first_name is None else first_name
        )
        self.last_name = (
            GenerateUser._fake.last_name() if last_name is None else last_name
        )
        self.email = GenerateUser._fake.email() if email is None else email
        self.password = GenerateUser._fake.password() if password is None else password
        self.phone = GenerateUser._fake.phone_number() if phone is None else phone
        self.user_status = random.choice([0, 1]) if user_status is None else user_status

    def build(self) -> UserSchema:
        return UserSchema(
            id=self.user_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            phone=self.phone,
            userStatus=self.user_status,
        )

    def build_payload(self) -> dict:
        return self.build().model_dump(by_alias=True, exclude_none=True)
