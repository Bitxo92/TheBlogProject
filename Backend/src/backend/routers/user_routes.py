from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..cruds.crud_user import UserCRUD
from ..schemas.user_schema import UserCreate, UserUpdate, UserRead

router = APIRouter(prefix="/users",tags=["Users"])

###############################################
# CREATE
###############################################
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserCRUD.create_user(db, user)

###############################################
# READ
###############################################
@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    return UserCRUD.get_user_by_id(db, user_id)

@router.get("/email/{email}", response_model=UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return UserCRUD.get_user_by_email(db, email)

@router.get("/username/{username}/id", response_model=UUID)
def get_user_id_by_username(username: str, db: Session = Depends(get_db)):
    return UserCRUD.get_user_id_by_username(db, username)

@router.get("/email/{email}/id", response_model=UUID)
def get_user_id_by_email(email: str, db: Session = Depends(get_db)):
    return UserCRUD.get_user_id_by_email(db, email)

@router.get("/", response_model=List[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    return UserCRUD.get_all_users(db)

###############################################
# UPDATE
###############################################
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    return UserCRUD.update_user(db, user_id, user_update)

###############################################
# DELETE
###############################################
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return {"message": UserCRUD.delete_user(db, user_id)}
