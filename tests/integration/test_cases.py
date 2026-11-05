from uuid import uuid4

from fastapi.testclient import TestClient

from apps.api.main import app


def test_duplicate_charge_case_can_be_reopened(tmp_path, monkeypatch):
    monkeypatch.setenv("OPSPILOT_CASE_DB", str(tmp_path / "cases.sqlite3"))
    message = "I was charged twice for my monthly membership. Can you help?"

    with TestClient(app) as client:
        response = client.post("/cases", json={"message": message})
        assert response.status_code == 201
        case = response.json()
        assert case["message"] == message

    with TestClient(app) as client:
        response = client.get(f"/cases/{case['id']}")
        assert response.status_code == 200
        assert response.json() == case
        assert client.get(f"/cases/{uuid4()}").status_code == 404
        assert client.post("/cases", json={"message": "   "}).status_code == 422


def test_case_can_open_synthetic_payment_history(tmp_path, monkeypatch):
    monkeypatch.setenv("OPSPILOT_CASE_DB", str(tmp_path / "cases.sqlite3"))

    with TestClient(app) as client:
        case = client.post("/cases", json={"message": "I was charged twice."}).json()
        response = client.get(f"/cases/{case['id']}/demo-customer")

        assert response.status_code == 200
        customer = response.json()
        assert customer["name"] == "Thinidu"
        assert customer["business"] == "Tunnel Express Car Wash"
        first, second = customer["payments"]
        assert first["id"] != second["id"]
        assert first["membership_period_start"] == second["membership_period_start"]
        assert first["amount_cents"] == second["amount_cents"] == 4900
        assert first["currency"] == second["currency"] == "AUD"
        assert client.get(f"/cases/{uuid4()}/demo-customer").status_code == 404
