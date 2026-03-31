from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_user(self, email: str, password_hash: str) -> User | None:
        try:
            user = User(email=email, password_hash=password_hash)
            self.session.add(user)
            await self.session.commit()
            return user
        except IntegrityError:
            await self.session.rollback()
            return

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_user_by_id(self, id: int) -> User | None:
        return await self.session.get(User, id)
    