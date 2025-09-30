from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
from .models.users import User 

import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    """Creates the database and tables."""
    SQLModel.metadata.create_all(engine)