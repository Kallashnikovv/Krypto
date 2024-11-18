from fastapi import FastAPI
from .routers.router_crypto import router

app = FastAPI()
app.include_router(router)