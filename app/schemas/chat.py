from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="Текст запроса")
    system: str | None = Field(None, description="Системная инструкция")
    int = Field(10, ge=1, le=50, description="Количество сообщений из истории")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Креативность модели")

class ChatResponse(BaseModel):
    answer: str
    