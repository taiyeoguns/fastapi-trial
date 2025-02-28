import factory
from factory.alchemy import SESSION_PERSISTENCE_COMMIT
from faker import Faker
from faker.providers import misc

from app.common.models import User

fake = Faker()
fake.add_provider(misc)


class DbModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_COMMIT


class UserFactory(DbModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())

    @factory.lazy_attribute
    def email(self):
        return f"{self.first_name}.{self.last_name}@fastapi-trial.local".lower()
