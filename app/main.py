import uvicorn

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from uuid import UUID

app = FastAPI()

test = [
    {
        "wallet_uuid": 1,
        "wallet_summ": 1100,
    },
    {
        "wallet_uuid": 2,
        "wallet_summ": 1200,
    },
    {
        "wallet_uuid": 3,
        "wallet_summ": 1300,
    },
]

def check_id_and_return_date(wallet_uuid: int) -> Dict[str, int] | None:
    """
    Функция для проверки наличия кошелька в базе данных и возврат из нее данных,
    если они там есть
    :param wallet_uuid: id кошелька для поиска и выдачи данных
    :return: Возвращает данные кошелька или False если их нет -> Dict[str, str | str]
    """
    for line in test:
        if line["wallet_uuid"] == wallet_uuid:
            return {
                "status": 200,
                "id": line["wallet_uuid"],
                "balance": line["wallet_summ"],
            }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wallet not found")


def change_wallet(wallet_uuid: int, operation: str, amount: int) -> Dict[str, int]:
    """

    :return: Dict[str, int]
    """
    pass


@app.get("/api/v1/wallets/{wallet_uuid}",
         summary="Получить информацию о кошельке",
         tags=['Кошелёк'])
async def get_wallet(wallet_uuid: int):
    date = check_id_and_return_date(wallet_uuid)

    return date


class WalletChange(BaseModel):
    operation_type: str
    amount: int


@app.post(
    path="/api/v1/wallets/{wallet_uuid}/operation",
    summary="Внести деньги в кошелёк",
    tags=['Кошелёк'])
async def post_operation_wallets(wallet_uuid:  int, request: WalletChange):
    wallet = check_id_and_return_date(wallet_uuid)

    method, summa = request.operation_type, request.amount
    if method == "DEPOSIT":
        wallet['balance'] += summa
    elif method == "WITHDRAW":
        if wallet["balance"] >= summa:
            wallet["balance"] =  wallet["balance"] - summa
            return {
                "status": 200,
                "id": wallet['wallet_uuid'],
                "balance": summa,
            }
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Unprocessable Entity")
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Unprocessable Entity")


    return wallet




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

