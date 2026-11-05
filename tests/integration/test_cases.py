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
