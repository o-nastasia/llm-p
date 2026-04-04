from app.repositories.users import UserRepo
from app.schemas.auth import TokenResponse
from app.core.security import create_access_token, hash_password, verify_password
from app.core.errors import ConflictError, AuthentificationError, NotFoundError
from app.schemas.user import UserPublic

class AuthUseCase:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo
    
    async def register(self, email: str, password: str) -> UserPublic:
        if await self.user_repo.get_user_by_email(email):
            raise ConflictError(
                message="Пользователь с таким email-ом уже существует",
            )
        password_hash = hash_password(password)
        user = await self.user_repo.add_user(email, password_hash)

        return UserPublic.model_validate(user)

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_user_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise AuthentificationError(
                message="Неверный логин или пароль",
            )
        
        access_token = create_access_token(str(user.id), user.role)

        return TokenResponse(access_token=access_token)
    
    async def user_by_id(self, id: int) -> UserPublic:
        user = await self.user_repo.get_user_by_id(id)
        if user is None:
            raise NotFoundError(
                message="Пользователь не найден",
            )
        
        return UserPublic.model_validate(user)
    