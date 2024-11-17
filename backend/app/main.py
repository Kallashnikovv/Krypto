from fastapi import FastAPI

from .routers.router import test_router

app = FastAPI()

app.include_router(test_router)