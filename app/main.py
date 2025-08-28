from fastapi import FastAPI
from app.api.v1.endpoints import orders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Desafio iPag - API de Pedidos",
    description="API para gerenciamento de pedidos, com processamento assíncrono de notificações.",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "API is running!"}