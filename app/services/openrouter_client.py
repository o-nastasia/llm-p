import httpx
from app.core.config import settings
from app.core.errors import ExternalServerError

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

    async def chat_completion(self, messages: list[dict], temperature: float = 0.7) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                }
            )

            if response.status_code != 200:
                raise ExternalServerError("OpenRouter API error")

            return response.json()["choices"][0]["message"]["content"]