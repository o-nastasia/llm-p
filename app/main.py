from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.db.session import async_engine
from app.db.base import Base
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.core.errors import AppBaseError

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppBaseError)
async def app_base_error_handler(request: Request, exc: AppBaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
