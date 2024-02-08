import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import db
from app.db.database import first_connection

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello World"}


origins = ["*"]


def main():
    db.init()

    app = FastAPI(
        title="VoiceAI",
        description="Voice AI",
        version="2"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def starup():
        # first connection for testing
        await first_connection()
        # await

    @app.on_event("shutdown")
    async def shutdown():
        asyncio.coroutine(db.close())

    from app.routers import auth, user

    app.include_router(auth.router)
    app.include_router(user.router)

    return app


app = main()

# @app.middleware('http')
# async def mw(
#         request: Request,
#         call_next: Callable[[Request], Awaitable[Response]]
# ) -> Response:
#     return await call_next(request)