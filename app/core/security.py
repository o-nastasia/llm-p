from passlib.context import CryptContext
from .config import settings
import jwt
import time

ACCESS_TTL_SECONDS = settings.access_token_expire_minutes * 60
ALGORITHM = settings.jwt_alg
SECRET_KEY = settings.jwt_secret

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хеширует пароль с помощью bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль его хешу."""
    return pwd_context.verify(password, hashed_password)

def now() -> int:
    """Возвращает текущее время в секундах."""
    return int(time.time())

def create_access_token(sub: str, role: str) -> str:
    """Создает JWT access token."""
    payload = {
        "sub": sub,
        "type": "access",
        "role": role,
        "iat": now(),
        "exp": now() + ACCESS_TTL_SECONDS
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict[str, any]:
    """Декодирует и валидирует JWT access token."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
