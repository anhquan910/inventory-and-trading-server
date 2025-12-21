from typing import Annotated
from fastapi import APIRouter, Depends
from app.schemas.user import User as UserPublic
from app.models.user import User as UserModel
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user