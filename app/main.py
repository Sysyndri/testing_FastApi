from email import message

import uvicorn
import uuid

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from uuid import UUID


from bd.create_test_date import create_test_date
from bd.bd import BD


app = FastAPI()

date_test_bd = create_test_date()
with open("test_date.txt", "w") as file:
    for date in date_test_bd:
        id = date['id']
        balance = date['wallet_balance']

        file.write(f"{id}\t{balance}\n")

bd_sql = BD()
bd_sql.create_table()
bd_sql.add_date(date_test_bd)


def check_id_and_return_date(wallet_uuid: UUID):
    """
    Функция для проверки наличия кошелька в базе данных и возврат из нее данных,
    если они там есть
    :param wallet_uuid: id кошелька для поиска и выдачи данных
    :return: Возвращает данные кошелька или False если их нет -> Dict[str, str | str]
    """
    wallet = bd_sql.get_wallet(wallet_uuid)

    if wallet:
        id, balance = wallet
        return {
            "status": 200,
            "id": UUID(bytes=id),
            "balance": balance
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
async def get_wallet(wallet_uuid: UUID):
    date = check_id_and_return_date(wallet_uuid)

    return date


class WalletChange(BaseModel):
    operation_type: str
    amount: int


@app.post(
    path="/api/v1/wallets/{wallet_uuid}/operation",
    summary="Внести деньги в кошелёк",
    tags=['Кошелёк'])
async def post_operation_wallets(wallet_uuid:  UUID, request: WalletChange):
    wallet = check_id_and_return_date(wallet_uuid)

    answer = None
    method, summa = request.operation_type, request.amount

    if method == "DEPOSIT":
        answer = bd_sql.change_wallet(wallet_uuid, summa, True)
    elif method == "WITHDRAW":
        answer = bd_sql.change_wallet(wallet_uuid, summa, False)


    if answer is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Unprocessable Entity",
        )


    return check_id_and_return_date(wallet_uuid)




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

