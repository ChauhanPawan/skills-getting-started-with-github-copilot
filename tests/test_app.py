import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_participants = {
        name: list(details["participants"])
        for name, details in app_module.activities.items()
    }
    yield
    for name, details in app_module.activities.items():
        details["participants"] = original_participants[name].copy()


def test_signup_updates_activity_participants():
    client = TestClient(app_module.app)

    response = client.post(
        "/activities/Chess Club/signup?email=test.student@mergington.edu"
    )

    assert response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200

    data = activities_response.json()
    assert "test.student@mergington.edu" in data["Chess Club"]["participants"]
