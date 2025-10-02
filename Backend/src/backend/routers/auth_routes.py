from select import select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..database import get_session
from ..models.users import User
from ..utils.security import verify_password, create_access_token, hash_password

# Router for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

###############################################
# Authentication Endpoints
###############################################
@router.post("/login", status_code=status.HTTP_200_OK)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(new_user: User, db: Session = Depends(get_session)):
    # Check if username already exists
    existing_username = db.exec(select(User).where(User.username == new_user.username)).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email already exists
    existing_email = db.exec(select(User).where(User.email == new_user.email)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    hashed_password = hash_password(new_user.password)

    # Create user object
    user = User(
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        password=hashed_password,
    )

    # Save user
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
