from app.repositories.chat_messages import MessageRepo
from app.services.openrouter_client import OpenRouterClient
from app.schemas.chat import ChatRequest, ChatResponse
from app.db.models import ChatMessage
from app.repositories.chat_messages import MessageRepo

class ChatUseCase:
    def __init__(self, message_repo: MessageRepo, or_client: OpenRouterClient) -> None:
        self.message_repo = message_repo
        self.or_client = or_client

    async def ask(self, user_id: int, prompt: str, system: str | None = None, max_history: int = 10, temperature: float = 0.7) -> str:
        pass




