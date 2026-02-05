from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta, datetime
import uuid
import os
from jose import jwt
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Get secret key from environment - provide a default for development if not set
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a new JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    """
    Authenticate user and return JWT token
    """
    try:
        # For now, simulate successful authentication
        # In a real app, you would verify the email/password against the database
        user_id = str(uuid.uuid4())  # Generate a user ID
        access_token = create_access_token(
            data={"sub": user_id, "email": request.email},
            expires_delta=timedelta(minutes=30)
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.post("/register", response_model=Token)
async def register(request: RegisterRequest):
    """
    Register a new user and return JWT token
    """
    try:
        # For now, just create a token without storing user
        # In a real app, you would store the user in the database
        user_id = str(uuid.uuid4())  # Generate a user ID
        access_token = create_access_token(
            data={"sub": user_id, "email": request.email},
            expires_delta=timedelta(minutes=30)
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )