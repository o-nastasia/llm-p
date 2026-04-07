from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ChatMessage
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

class MessageRepo:
    """Репозиторий для работы с сообщениями чата."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, content: str, role: str, user_id: int) -> ChatMessage | None:
        """Сохраняет новое сообщение."""
        try:
            message = ChatMessage(content=content, role=role, user_id = user_id)
            self.session.add(message)
            await self.session.commit()
            return message
        except IntegrityError:
            await self.session.rollback()
            return

    async def get_n_messages(self, n: int, user_id: int) -> list[ChatMessage]:
        """Возвращает последние N сообщений пользователя."""
        result = await self.session.execute(select(ChatMessage).where(ChatMessage.user_id == user_id).order_by(ChatMessage.created_at.desc()).limit(n))
        return list(result.scalars().all())
    
    async def delete_history(self, user_id: int) -> None:
        """Удаляет всю историю сообщений пользователя."""
        await self.session.execute(delete(ChatMessage).where(ChatMessage.user_id == user_id))
        await self.session.commit()
        return
    