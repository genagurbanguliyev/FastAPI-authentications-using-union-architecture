import asyncio
from typing import Any

from fastapi import APIRouter

from app.schema.global_schema import ResponseSchema
from app.service.auth_service import AuthService
from app.schema.user_schema import RegisterSchema, UserBaseSchema

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/registration", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await AuthService.register_service(request_body)
    return ResponseSchema(detail="Successfully save data!")


@router.post('/login', response_model=ResponseSchema)
async def login(request_body: UserBaseSchema) -> Any:
    token = asyncio.run(AuthService.login_service(request_body))
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})