from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.repository.users_repo import UsersRepo


class UserService:

    @staticmethod
    async def get_user_profile(username: str):
        _username = await UsersRepo.find_by_username(username)
        if _username is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Username {username} not found",
            )
        else:
            return jsonable_encoder(_username)