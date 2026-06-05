"""Authentication routes for the compiler API."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory user storage (replace with database in production)
users_db = {}
active_tokens = {}


class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user: dict


@router.post("/signup")
async def signup(request: SignUpRequest):
    """Register a new user."""
    if request.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Store user (in production, hash the password!)
    users_db[request.email] = {
        "name": request.name,
        "email": request.email,
        "password": request.password
    }
    
    # Generate a simple token (in production, use JWT)
    token = f"token_{len(active_tokens) + 1}"
    active_tokens[token] = request.email
    
    return AuthResponse(
        token=token,
        user={
            "name": request.name,
            "email": request.email
        }
    )


@router.post("/signin")
async def signin(request: SignInRequest):
    """Sign in an existing user."""
    user = users_db.get(request.email)
    
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate token
    token = f"token_{len(active_tokens) + 1}"
    active_tokens[token] = request.email
    
    return AuthResponse(
        token=token,
        user={
            "name": user["name"],
            "email": user["email"]
        }
    )


@router.post("/logout")
async def logout(token: str):
    """Sign out a user."""
    if token in active_tokens:
        del active_tokens[token]
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(token: str):
    """Get current user info from token."""
    if token not in active_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    email = active_tokens[token]
    user = users_db.get(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "name": user["name"],
        "email": user["email"]
    }
