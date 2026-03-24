class AppBaseError(Exception):
    """Базовая ошибка приложения."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class ConflictError(AppBaseError):
    """Ошибка конфликта."""
    pass

class AuthorisationError(AppBaseError):
    """Ошибка авторизации."""
    pass

class AuthentificationError(AppBaseError):
    """Ошибка аутентификации."""
    pass

class NotFoundError(AppBaseError):
    """Ошибка поиска."""
    pass

class ExternalServerError(AppBaseError):
    """Ошибка внешнего сервера."""
    pass
