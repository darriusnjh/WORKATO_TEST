from fastapi import FastAPI, HTTPException, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime, timedelta
import pytz
from pathlib import Path
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI(title="Calculator API", version="1.0.0")

# Setup templates directory
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Authentication configuration
SECRET_KEY = "your-secret-key-keep-it-secret-in-production-use-env-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing - using SHA256 for compatibility
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# In-memory user database (in production, use a real database)
users_db = {}


# Pydantic models
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: User


# Authentication utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username: str) -> Optional[UserInDB]:
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(username=user.username, email=user.email, full_name=user.full_name)


class CalculatorRequest(BaseModel):
    operation: Literal["+", "-", "*", "/"]
    num1: float
    num2: float


class CalculatorResponse(BaseModel):
    operation: str
    num1: float
    num2: float
    result: float


@app.get("/")
def read_root():
    return {"message": "Calculator API is running. Use /calculate endpoint for operations."}


@app.post("/calculate", response_model=CalculatorResponse)
def calculate(request: CalculatorRequest):
    """
    Perform calculator operations: addition (+), subtraction (-), multiplication (*), division (/)
    """
    num1 = request.num1
    num2 = request.num2
    operation = request.operation

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = num1 / num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return CalculatorResponse(
        operation=operation,
        num1=num1,
        num2=num2,
        result=result
    )


@app.get("/clock", response_class=HTMLResponse)
async def digital_clock(request: Request, timezone: str = "UTC"):
    """
    Display a digital clock with real-time updates.
    Supports multiple timezones via the timezone query parameter.

    Examples:
    - /clock (displays UTC time)
    - /clock?timezone=America/New_York
    - /clock?timezone=Asia/Singapore
    """
    try:
        # Validate timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)

        return templates.TemplateResponse(
            "clock.html",
            {
                "request": request,
                "timezone": timezone,
                "current_time": current_time.strftime("%H:%M:%S"),
                "current_date": current_time.strftime("%A, %B %d, %Y"),
            }
        )
    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid timezone: {timezone}. Please use a valid IANA timezone name."
        )


# Authentication endpoints
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display the login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Display the registration page"""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/api/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate):
    """
    Register a new user with secure password hashing
    """
    # Check if user already exists
    if user_create.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    for user_data in users_db.values():
        if user_data["email"] == user_create.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Hash password and store user
    hashed_password = get_password_hash(user_create.password)
    user_dict = {
        "username": user_create.username,
        "email": user_create.email,
        "full_name": user_create.full_name,
        "hashed_password": hashed_password
    }
    users_db[user_create.username] = user_dict

    return User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name
    )


@app.post("/api/login", response_model=LoginResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Authenticate user and return JWT token
    """
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(
        message="Login successful",
        access_token=access_token,
        token_type="bearer",
        user=User(username=user.username, email=user.email, full_name=user.full_name)
    )


@app.get("/api/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile (protected route)
    """
    return current_user


@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """Display the profile page (requires authentication)"""
    return templates.TemplateResponse("profile.html", {"request": request})

