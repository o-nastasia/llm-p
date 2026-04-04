from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat, get_current_user_id

router = APIRouter()

@router.post("/", response_model = ChatResponse)
async def chat_response(request: ChatRequest, user_id: int = Depends(get_current_user_id), chat_usecase: ChatUseCase = Depends(get_chat)) -> ChatResponse:
    """Отправляет запрос к LLM и возвращает ответ."""
    answer = await chat_usecase.ask(user_id, request.prompt, request.system, request.history, request.temperature)
    return ChatResponse(answer=answer)

@router.get("/history", response_model=list[ChatHistoryResponse])
async def get_chat_history(user_id: int = Depends(get_current_user_id), chat_usecase: ChatUseCase = Depends(get_chat), limit: int = 10) ->list[ChatHistoryResponse]:
    """Возвращает историю сообщений пользователя."""
    history = await chat_usecase.get_history(user_id, limit)
    return history

@router.delete("/history", status_code=204)
async def delete_history(user_id: int = Depends(get_current_user_id), chat_usecase: ChatUseCase = Depends(get_chat)):
    """Удаляет всю историю сообщений пользователя."""
    await chat_usecase.delete_history(user_id)
    return