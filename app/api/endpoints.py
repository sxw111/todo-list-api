from fastapi import APIRouter

from app.api.routers.auth import router as auth_router
from app.api.routers.todos import router as todos_router
from app.api.routers.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(todos_router, prefix="/todos", tags=["ToDo's"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
