from fastapi import FastAPI
from fastapi.responses import FileResponse

from typing import Dict

app = FastAPI()

@app.get("/api/v1/wallets/{wallet_uuid}")
async def get_wallet(wallet_uuid: int):
    return {"wallet_uuid": wallet_uuid}


@app.post("/api/v1/wallets/{wallet_uuid}/{operation}")
async def post_operation_waller(wallet_uuid: int, operation: Dict[str, str]):
    return wallet_uuid, operation

