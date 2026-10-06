from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_post_operation_correct() -> None:
    date = {
        "operation_type": "DEPOSIT",
        "amount": 1000,
    }

    response = client.post("/api/v1/wallets/2/operation", json=date)

    assert response.status_code == 200