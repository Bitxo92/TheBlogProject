from datetime import datetime
from uuid import UUID,uuid4
from pydantic import EmailStr
from sqlmodel import SQLModel,Field

class User(SQLModel,table = True):
    __tablename__ = "USERS"
    __description__ = "User model representing a user in the system."
        
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)
    updated_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)