from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
from .models.users import User 
import os

###############################################
# Database Configuration
###############################################
load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)

###############################################
# Database Helper Functions
###############################################

def get_session():
    """Creates a new database session."""
    from sqlmodel import Session
    with Session(engine) as session:
        yield session
    


def create_db_and_tables():
    """Creates the database and tables."""
    SQLModel.metadata.create_all(engine)