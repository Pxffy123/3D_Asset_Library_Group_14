import pytest

from app import create_app
from extensions import db
from models import User, Asset


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "JWT_SECRET_KEY": "test-secret-key-for-asset-library-tests-2026"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    client.post("/signup", json={
        "username": "testuser",
        "password": "Test123!",
        "password_confirmation": "Test123!"
    })

    response = client.post("/login", json={
        "username": "testuser",
        "password": "Test123!"
    })

    token = response.json["token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_signup(client):
    response = client.post("/signup", json={
        "username": "newuser",
        "password": "Test123!",
        "password_confirmation": "Test123!"
    })

    assert response.status_code == 201
    assert response.json["user"]["username"] == "newuser"


def test_duplicate_signup(client):
    data = {
        "username": "testuser",
        "password": "Test123!",
        "password_confirmation": "Test123!"
    }

    client.post("/signup", json=data)
    response = client.post("/signup", json=data)

    assert response.status_code == 409


def test_login(client):
    client.post("/signup", json={
        "username": "testuser",
        "password": "Test123!",
        "password_confirmation": "Test123!"
    })

    response = client.post("/login", json={
        "username": "testuser",
        "password": "Test123!"
    })

    assert response.status_code == 200
    assert "token" in response.json


def test_me_requires_authentication(client):
    response = client.get("/me")

    assert response.status_code == 401


def test_create_asset(client, auth_headers):
    response = client.post("/assets", headers=auth_headers, json={
        "name": "Test Character",
        "description": "A test 3D character",
        "category": "character",
        "format": "BLEND"
    })

    assert response.status_code == 201
    assert response.json["name"] == "Test Character"


def test_get_assets(client, auth_headers):
    client.post("/assets", headers=auth_headers, json={
        "name": "Test Asset",
        "description": "Asset description",
        "category": "environment",
        "format": "FBX"
    })

    response = client.get("/assets", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json["items"]) == 1


def test_update_asset(client, auth_headers):
    created = client.post("/assets", headers=auth_headers, json={
        "name": "Original Name",
        "description": "Original description",
        "category": "character",
        "format": "BLEND"
    })

    asset_id = created.json["id"]

    response = client.patch(
        f"/assets/{asset_id}",
        headers=auth_headers,
        json={"name": "Updated Name"}
    )

    assert response.status_code == 200
    assert response.json["name"] == "Updated Name"


def test_delete_asset(client, auth_headers):
    created = client.post("/assets", headers=auth_headers, json={
        "name": "Delete Me",
        "description": "Temporary asset",
        "category": "material",
        "format": "OBJ"
    })

    asset_id = created.json["id"]

    response = client.delete(
        f"/assets/{asset_id}",
        headers=auth_headers
    )

    assert response.status_code == 204


def test_user_cannot_access_another_users_asset(client):
    # Create first user and their asset
    client.post("/signup", json={
        "username": "userone",
        "password": "Test123!",
        "password_confirmation": "Test123!"
    })

    login_one = client.post("/login", json={
        "username": "userone",
        "password": "Test123!"
    })

    token_one = login_one.json["token"]
    headers_one = {"Authorization": f"Bearer {token_one}"}

    created = client.post("/assets", headers=headers_one, json={
        "name": "Private Asset",
        "description": "Belongs to user one",
        "category": "character",
        "format": "BLEND"
    })

    asset_id = created.json["id"]

    # Create second user
    client.post("/signup", json={
        "username": "usertwo",
        "password": "Test123!",
        "password_confirmation": "Test123!"
    })

    login_two = client.post("/login", json={
        "username": "usertwo",
        "password": "Test123!"
    })

    token_two = login_two.json["token"]
    headers_two = {"Authorization": f"Bearer {token_two}"}

    # User two attempts to update user one's asset
    response = client.patch(
        f"/assets/{asset_id}",
        headers=headers_two,
        json={"name": "Hacked"}
    )

    assert response.status_code == 404