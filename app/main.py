import uvicorn
from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.base_config import auth_backend, fastapi_users
from app.auth.router import auth_router
from app.auth.schemas import UserRead, UserCreate
from app.chat.router import chat_router
from app.operations.router import operation_router
from app.config import settings
from app.pages.router import pages_router
from app.tasks.router import tasks_router

app = FastAPI(
    title="Trading App"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(settings.REDIS_HOST, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(auth_router)
app.include_router(operation_router)
app.include_router(tasks_router)
app.include_router(pages_router)
app.include_router(chat_router)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
