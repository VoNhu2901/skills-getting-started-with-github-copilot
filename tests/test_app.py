import sys
import copy

# Ensure `src` is importable so we can import the FastAPI app
sys.path.insert(0, "src")

from app import app, activities
from fastapi.testclient import TestClient


@property
def _client():
    return TestClient(app)


def reset_activities(original):
    activities.clear()
    activities.update(original)


def test_get_activities():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect a known activity to exist
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    original = copy.deepcopy(activities)
    client = TestClient(app)
    email = "test.student@example.com"
    activity_name = "Basketball"

    # Ensure not already signed up
    if email in activities.get(activity_name, {}).get("participants", []):
        activities[activity_name]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Unregister
    resp2 = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert resp2.status_code == 200
    assert email not in activities[activity_name]["participants"]

    # restore original state
    reset_activities(original)
