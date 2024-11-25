from fastapi import FastAPI
from .routers.router_crypto import router as router_crypto
from .routers.router_forex import router as router_forex

app = FastAPI()
app.include_router(router_crypto)
app.include_router(router_forex)

