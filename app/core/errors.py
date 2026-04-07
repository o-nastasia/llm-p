from fastapi import status

class AppBaseError(Exception):
    """Базовая ошибка приложения."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ConflictError(AppBaseError):
    """Ошибка конфликта."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


class AuthorisationError(AppBaseError):
    """Ошибка авторизации."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class AuthentificationError(AppBaseError):
    """Ошибка аутентификации."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class NotFoundError(AppBaseError):
    """Ошибка поиска."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class ExternalServerError(AppBaseError):
    """Ошибка внешнего сервера."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_502_BAD_GATEWAY)
