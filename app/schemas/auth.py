from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=128)
