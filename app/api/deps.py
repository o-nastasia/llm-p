from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.users import UserRepo
from app.repositories.chat_messages import MessageRepo
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.services.openrouter_client import OpenRouterClient

async def get_db_session():
    """Создает и закрывает сессию базы данных для каждого запроса."""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

async def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()
    
async def get_user_repo(session: AsyncSession = Depends(get_db_session)) -> UserRepo:
    return UserRepo(session)

async def get_message_repo(session: AsyncSession = Depends(get_db_session)) -> MessageRepo:
    return MessageRepo(session)

async def get_auth(user_repo: UserRepo = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)

async def get_chat(message_repo: MessageRepo = Depends(get_message_repo), openrouter_client: OpenRouterClient = Depends(get_openrouter_client)) -> ChatUseCase:
    return ChatUseCase(message_repo, openrouter_client)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Извлекает user_id из JWT токена."""
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Токен недействителен")
        return int(user_id)
    except Exception:
        raise HTTPException(status_code=401, detail="Токен недействителен")
    