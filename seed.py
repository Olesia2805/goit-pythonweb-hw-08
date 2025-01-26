from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.conf.config import Config
from src.database.models import Base, Contact
from faker import Faker
import asyncio

fake = Faker()

engine = create_async_engine(Config.DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def seed_database():
    async with async_session() as session:
        async with session.begin():
            for _ in range(25):
                contact = Contact(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    phone_number=fake.msisdn(),
                    birthday=fake.date_of_birth(minimum_age=1, maximum_age=70),
                    additional_data=fake.sentence(nb_words=3),
                )
                session.add(contact)


if __name__ == "__main__":

    asyncio.run(seed_database())
