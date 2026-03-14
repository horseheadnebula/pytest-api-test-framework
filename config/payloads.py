import random

from faker import Faker

from models.pet_model import Category, PetSchema, Tags


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
