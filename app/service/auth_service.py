from fastapi import status, HTTPException

from app.db.models import Users
from app.schema.user_schema import RegisterSchema, UserBaseSchema
from app.repository.auth_repo import JWTRepo
from app.views.pwd_hashing import pwd_context
from app.repository.users_repo import UsersRepo

from fastapi.encoders import jsonable_encoder


class AuthService:

    @staticmethod
    async def register_service(register: RegisterSchema):
        # mapping request data to class entity table
        _user = Users(username=register.username, password=pwd_context.hash(register.password), role=register.role)

        # checking the same username
        _username = await UsersRepo.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {register.username} already exists",
            )
        else:
            # parent_data = jsonable_encoder(_user)
            # Insert to table
            await UsersRepo.create(**jsonable_encoder(_user))

    @staticmethod
    async def login_service(login: UserBaseSchema):
        _username = await UsersRepo.find_by_username(login.username)

        if _username is not None:
            if not pwd_context.verify(login.password, _username.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Incorrect password",
                )
            return JWTRepo(data={"username": login.username}).generate_token()
        raise HTTPException(status_code=404, detail="Username not found !")