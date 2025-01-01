from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import oauth

client = TestClient(app)


def test_oauth_config():
    """Test that OAuth is configured correctly"""
    assert oauth.github.client_id is not None and oauth.github.client_id != ""
    assert oauth.github.client_secret is not None and oauth.github.client_secret != ""


def test_auth_endpoints_exist():
    """Test that our auth endpoints are properly configured"""
    # Test both sync and async test endpoints
    response = client.get("/api/v1/auth/test")
    print(f"Async test endpoint response status: {response.status_code}")
    print(f"Async test endpoint response body: {response.text}")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    response = client.get("/api/v1/auth/test2")
    print(f"Sync test endpoint response status: {response.status_code}")
    print(f"Sync test endpoint response body: {response.text}")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Print all available routes for debugging
    print("\nAvailable routes:")
    for route in app.routes:
        print(f"Route: {route.path} [{route.methods}]")

    # Then test the GitHub login endpoint with test-mode header
    print("\nTesting GitHub login endpoint:")
    response = client.get("/api/v1/auth/login/github", headers={"test-mode": "true"})
    print(f"GitHub login response status: {response.status_code}")
    print(f"GitHub login response body: {response.text}")
    assert response.status_code == 200
    assert response.json() == {"status": "route works"}


def test_auth_callback_endpoints_exist():
    """Test that our callback endpoints are properly configured"""
    response = client.get("/api/v1/auth/github/callback")
    assert response.status_code in [400, 401]  # Should fail without proper OAuth state
