import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.config import settings
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
        # create folders for uploading files
        # settings.make_dirs()

        # first connection for testing
        # with hypercorn trio
        # asyncio.run(first_connection())

        # with uvicorn
        await first_connection()

    @app.on_event("shutdown")
    async def shutdown():
        # with hypercorn trio
        # asyncio.run(db.close())

        # with uvicorn
        await db.close()

    from app.routers import auth, user, uploads

    # Mounting paths
    app.mount("/audio", StaticFiles(directory="audio"), name="audio")

    # Routers
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(uploads.router)

    return app


app = main()

# @app.middleware('http')
# async def mw(
#         request: Request,
#         call_next: Callable[[Request], Awaitable[Response]]
# ) -> Response:
#     return await call_next(request)