from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Security settings
SECRET_KEY = "your_secret_key"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the provided password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(user_id: int, email: str, role: str, expires_delta: timedelta = None):
    """Create a JWT access token with expiration time, including user ID."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": str(user_id),  # ✅ Make sure ID is included as a string
        "email": email,
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user details from the JWT token, including user ID."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # ✅ Extract user ID
        user_email = payload.get("email")
        user_role = payload.get("role")  # Ensure role is included

        if not user_id or not user_email or not user_role:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return {"id": user_id, "email": user_email, "role": user_role}  # ✅ Include "id"

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")


def require_role(required_role: str):
    """Dependency to check if a user has the correct role."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=403, detail=f"Access forbidden: {required_role}s only.")
        return current_user
    return role_checker
