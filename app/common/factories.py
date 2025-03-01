import factory
from factory.alchemy import SESSION_PERSISTENCE_COMMIT
from faker import Faker
from faker.providers import misc

from app.common.models import User
from sqlalchemy.orm import Session

fake = Faker()
fake.add_provider(misc)


class DbModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_COMMIT

    @classmethod
    def create_instances(cls, session: Session, size: int = 1, **kwargs):
        cls._meta.sqlalchemy_session = session
        return cls.create_batch(size=size, **kwargs)

    @classmethod
    def create_instance(cls, session: Session, **kwargs):
        return cls.create_instances(session, size=1, **kwargs)[0]


class UserFactory(DbModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())

    @factory.lazy_attribute
    def email(self):
        return f"{self.first_name}.{self.last_name}@fastapi-trial.local".lower()
