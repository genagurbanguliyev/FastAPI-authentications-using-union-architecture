# import uvicorn
import asyncio

from hypercorn.config import Config
from hypercorn.asyncio import serve

import trio
# from hypercorn.trio import serve

from app.main import app

if __name__ == "__main__":
    # RunServer using uvicorn:

    # uvicorn.run(
    #     "app.main:app",
    #     # host="192.168.192.24",
    #     port=8000,
    #     # log_level="info",
    #     reload=True
    # )

    config = Config()
    config.bind = ["localhost:8000"]

    # Run server with hypercorn:
    asyncio.run(serve(app, config))

    # Run server with hypercorn with trio:
    # trio.run(serve, app, config)