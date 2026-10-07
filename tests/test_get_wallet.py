from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_walid_id() -> None:
    response = client.get("/api/v1/wallets/88e4a433-e1f0-498f-b878-8697007095d0")
    assert response.status_code == 200


def test_invalid_id() -> None:
    response = client.get("/api/v1/wallets/5")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "wallet not found"
    }
