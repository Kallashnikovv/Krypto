from fastapi import FastAPI
from app.routers.router_crypto import router as router_crypto
from app.routers.router_forex import router as router_forex

#app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()

app.include_router(router_crypto, prefix="/crypto")
app.include_router(router_forex, prefix="/forex")
