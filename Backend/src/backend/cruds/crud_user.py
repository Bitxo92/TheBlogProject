from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models.users import User
from ..schemas.user_schema import *
from fastapi import HTTPException, status
from datetime import datetime, timezone, timezone

class UserCRUD:
    """ CRUD operations for User model """

###############################################
# CREATE
###############################################
 
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Creates a new user in the database.

        Args:
            db (Session): Database session
            user (UserCreate): pydantic model for creating a user

        Raises:
            HTTPException: If user with this email or username already exists
     

        Returns:
            User: The created user
        """
        new_user = User(**user.model_dump())
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError as e:
            db.rollback()
            if 'UNIQUE constraint failed: users.username' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered",
                )
            elif 'UNIQUE constraint failed: users.email' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )

        return new_user
    
###############################################
# GETTERS
###############################################

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User | None:
        """Fetch a user by ID.

        Args:
            db (Session): Database session
            user_id (UUID): User ID type UUID

        Raises:
            HTTPException: If user not found

        Returns:
            User | None: The user object or None if not found
        """
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Fetch a user by email.

        Args:
            db (Session): Database Session
            email (str): User email

        Raises:
            HTTPException: If user not found

        Returns:
            User | None: The user object or None if not found
        """
        stmt = select(User).where(User.email == email)
        user = db.exec(stmt).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    @staticmethod
    def get_user_id_by_username(db: Session, username: str) -> UUID | None:
        """Fetch a user ID by username.

        Args:
            db (Session): Database Session
            username (str): User username

        Raises:
            HTTPException: If user not found

        Returns:
            UUID | None: The user ID or None if not found
        """
        stmt = select(User).where(User.username == username)
        user = db.exec(stmt).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user.id
    
    @staticmethod
    def get_user_id_by_email(db: Session, email: str) -> UUID | None:
        """Fetch a user ID by email.

        Args:
            db (Session): Database Session
            email (str): User email

        Raises:
            HTTPException: If user not found

        Returns:
            UUID | None: The user ID or None if not found
        """
        stmt = select(User).where(User.email == email)
        user = db.exec(stmt).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user.id
    
    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        """Fetch all users from the database.

        Args:
            db (Session): Database Session

        Raises:
            HTTPException: If no users found

        Returns:
            list[User]: List of all user objects
        """
        users = db.exec(select(User)).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return users

###############################################
# UPDATE
###############################################

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> User | None:
        """Update a user in the database.

        Args:
            db (Session): Database Session
            user_id (UUID): user ID type UUID
            user_update (UserUpdate): Pydantic model for updating a user

        Raises:
            HTTPException: If user not found

        Returns:
            User | None: The updated user object or None if not found
        """
        db_user = db.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db_user.updated_at = datetime.now(timezone.utc)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

###############################################
# DELETE
###############################################

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> str:
        """Delete a user from the database.

        Args:
            db (Session): Database Session
            user_id (UUID): user ID type UUID

        Raises:
            HTTPException: If user not found

        Returns:
            str: Success message
        """
        db_user = db.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.delete(db_user)
        db.commit()
        return f"User {db_user.username} with email: {db_user.email} deleted successfully"
