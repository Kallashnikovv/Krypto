from fastapi import FastAPI
from app.routers.router_crypto import router as router_crypto
from app.routers.router_forex import router as router_forex

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Dodaj middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Zezwolenie na dostęp z frontend na porcie 3000
    allow_credentials=True,
    allow_methods=["*"],  # Zezwolenie na wszystkie metody
    allow_headers=["*"],  # Zezwolenie na wszystkie nagłówki
)

# Włącz routery
app.include_router(router_crypto, prefix="/crypto")
app.include_router(router_forex, prefix="/forex")
