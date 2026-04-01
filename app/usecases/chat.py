from app.repositories.chat_messages import MessageRepo
from app.services.openrouter_client import OpenRouterClient

class ChatUseCase:
    def __init__(self, message_repo: MessageRepo, or_client: OpenRouterClient) -> None:
        self.message_repo = message_repo
        self.or_client = or_client

    async def ask(self, user_id: int, prompt: str, system: str | None = None, max_history: int = 10, temperature: float = 0.7) -> str:
        context = await self.message_repo.get_n_messages(max_history, user_id)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        for msg in context:
            messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": prompt})
        
        await self.message_repo.add_message(prompt, 'user', user_id)

        answer = await self.or_client.chat_completion(messages, temperature)
        await self.message_repo.add_message(answer, 'assistant' ,user_id)

        return answer
