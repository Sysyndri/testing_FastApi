import uvicorn

from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.get("/api/v1/wallets/{wallet_uuid}",
         summary="Получить информацию о кошельке",
         tags=['Кошелёк'])
async def get_wallet(wallet_uuid: int):
    return {"wallet_uuid": wallet_uuid}


@app.post("/api/v1/wallets/{wallet_uuid}/{operation}",
          summary="Внести деньги в кошелёк",
          tags=['Кошелёк'])
async def post_operation_waller(wallet_uuid: int, operation):
    return wallet_uuid, operation



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

