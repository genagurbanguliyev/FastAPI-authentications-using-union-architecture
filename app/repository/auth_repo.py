from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.config import settings


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/log")


class JWTRepo:

    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def generate_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = self.data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def decode_token(self):
        try:
            decode_token = jwt.decode(
                self.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except:
            return {}

    @staticmethod
    def extract_token(token: str):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # @staticmethod
    # async def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #         username: str = payload.get("sub")
    #         user_id: int = payload.get("id")
    #         if username is None or user_id is None:
    #             raise status.HTTP_401_UNAUTHORIZED
    #         return {"username": username, "id": user_id}
    #     except JWTError:
    #         raise status.HTTP_401_UNAUTHORIZED


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})

    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return True if decoded is not None else False
        except JWTError:
            return False