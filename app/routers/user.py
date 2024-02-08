import asyncio

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.schema.global_schema import ResponseSchema
from app.service.users import UserService
from app.repository.auth_repo import JWTBearer, JWTRepo

router = APIRouter(
    prefix="/api/v1/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    result = asyncio.run(UserService.get_user_profile(token['username']))
    return ResponseSchema(detail="Successfully fetch data!", result=result)