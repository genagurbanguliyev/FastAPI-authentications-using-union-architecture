from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jose import jwt, JWTError
from starlette import status

from app.config import settings

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise status.HTTP_401_UNAUTHORIZED
        return {"username": username, "id": user_id}
    except JWTError:
        raise status.HTTP_401_UNAUTHORIZED