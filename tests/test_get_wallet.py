from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_walid_id() -> None:
    response = client.get("/api/v1/wallets/2")
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "id": 1,
        "balance": 1100,
    }


def test_invalid_id() -> None:
    response = client.get("/api/v1/wallets/5")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "wallet not found"
    }
