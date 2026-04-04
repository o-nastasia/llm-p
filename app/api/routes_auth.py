from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth, get_current_user_id

router = APIRouter()

@router.post("/register", response_model=UserPublic)
async def register(request: RegisterRequest, auth_usecase: AuthUseCase = Depends(get_auth)) -> UserPublic:
    user = await auth_usecase.register(request.email, request.password)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(request: OAuth2PasswordRequestForm = Depends(), auth_usecase: AuthUseCase = Depends(get_auth)) -> TokenResponse:
    token = await auth_usecase.login(request.username, request.password)
    return token

@router.get("/me", response_model=UserPublic)
async def show_profile(user_id: int = Depends(get_current_user_id), auth_usecase: AuthUseCase = Depends(get_auth)) -> UserPublic:
    user = await auth_usecase.user_by_id(user_id)
    return user
