import pytest
from app import create_app
from app.extensions import db
from app.utils.seed import seed_data
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        
@pytest.fixture()
def client(app):
    return app.test_client()        

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def admin_auth_headers(client):
    credentials = {
        "username": "John Smith",
        "password_hash": "abcdfghjkl"
    }
    
    response = client.post(
        "/api/v1/auth/login",
        json = credentials,
        content_type = "application/json"
    )
    
    token = response.get_json()["access_token"]
    
    header = {"Authorization": f"Bearer {token}"}
    return header

@pytest.fixture()
def user_auth_headers(client):
    credentials = {
        "username": "Jane Miranda",
        "password_hash": "jane34678_23"
    }
    
    response = client.post(
        "/api/v1/auth/login",
        json = credentials,
        content_type = "application/json"
    )
    
    token = response.get_json()["access_token"]
    
    header = {"Authorization": f"Bearer {token}"}
    return header

    
