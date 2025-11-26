import pytest
import httpx

BASE_URL = "http://localhost:8000/api/v1"

@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client

def test_register_and_login(client):
    # Register new user
    resp = client.post("/auth/register", json={
        "email": "pytestuser@example.com",
        "password": "Test@1234",
        "first_name": "Py",
        "last_name": "Test"
    })
    assert resp.status_code == 201

    # Login user
    resp = client.post("/auth/login", json={
        "email": "pytestuser@example.com",
        "password": "Test@1234"
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    user_id = resp.json()["user_id"]
    assert token
    assert user_id
    client.headers["Authorization"] = f"Bearer {token}"

    # Update user profile
    resp = client.put(f"/users/{user_id}", json={
        "skin_type": "normal",
        "skin_concerns": ["dryness"],
        "age": 30,
        "gender": "male"
    })
    assert resp.status_code == 200

    # Run skin analysis (simulate img)
    img_str = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    resp = client.post("/analysis/analyze", json={"image_data": img_str, "user_id": user_id})
    assert resp.status_code == 200
    assert "skin_condition" in resp.json()

    # Scan product ingredients
    resp = client.post("/ingredients/scan", json={
        "product_name": "Foam Cleanser",
        "ingredients": ["Water", "Sodium Cocoyl Glycinate"]
    })
    assert resp.status_code == 200
    assert "safety_rating" in resp.json()

    # Create skincare routine
    resp = client.post("/routine/create", json={
        "user_id": user_id,
        "skin_type": "normal"
    })
    assert resp.status_code == 200

    # Update & fetch progress
    resp = client.post("/progress/update", json={
        "user_id": user_id,
        "metric": "hydration",
        "value": 7.9
    })
    assert resp.status_code == 200
    resp = client.get(f"/progress/metrics?user_id={user_id}")
    assert resp.status_code == 200

    # Send & fetch notifications
    resp = client.post("/notifications/push", json={
        "user_id": user_id,
        "title": "Test",
        "body": "Integration test alert",
        "type": "test"
    })
    assert resp.status_code == 200
    resp = client.get(f"/notifications?user_id={user_id}")
    assert resp.status_code == 200

    # Book consultation (skip if no slots)
    resp = client.get("/dermatologist/available?date=2024-01-20")
    assert resp.status_code == 200
    slots = resp.json()
    if slots:
        slot_id = slots[0]["slot_id"]
        resp = client.post("/dermatologist/book", json={
            "user_id": user_id,
            "slot_id": slot_id,
            "reason": "Test consult"
        })
        assert resp.status_code == 200
