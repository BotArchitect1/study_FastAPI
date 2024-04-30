from fastapi import Depends, APIRouter

from app.auth.base_config import current_user
from app.auth.models import User


auth_router = APIRouter(
    prefix="/let",
    tags=["Trade"]
)


@auth_router.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@auth_router.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

