from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class UserRepo:
    """Репозиторий для работы с пользователями."""
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_user(self, email: str, password_hash: str) -> User | None:
        """Создает нового пользователя."""
        try:
            user = User(email=email, password_hash=password_hash)
            self.session.add(user)
            await self.session.commit()
            return user
        except IntegrityError:
            await self.session.rollback()
            return

    async def get_user_by_email(self, email: str) -> User | None:
        """Возвращает пользователя по email."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_user_by_id(self, id: int) -> User | None:
        """Возвращает пользователя по id."""
        return await self.session.get(User, id)
    