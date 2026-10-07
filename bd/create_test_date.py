from typing import List, Dict
from uuid import UUID
from uuid import uuid4
from random import randint


def create_test_date() -> List[Dict[str, UUID | int]]:
    date = []

    for ind in range(100):
        id = uuid4()
        balance = randint(100, 100_000)

        date.append({"id": id, "wallet_balance": balance})

    return date

