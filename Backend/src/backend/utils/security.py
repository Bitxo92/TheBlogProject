import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt

###############################################
# Environment Variables
###############################################
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


###############################################
# JWT Token Management
###############################################

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a new access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    """Verifies an access token and returns the decoded data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid token")



###############################################
# Password Hashing and Verification
###############################################

def hash_password(password: str) -> str:
    """Hashes a plaintext password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a hashed password against a plaintext password."""
    return pwd_context.verify(plain_password, hashed_password)
