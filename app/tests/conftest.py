from app.containers.user_container import User_DI
from app.containers.project_container import Project_DI
from app.containers.task_container import Task_DI
from app.extensions import db
from app import create_app
import pytest

@pytest.fixture()
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
def admin_auth_headers(client):
    credentials = {
        "username": "John Smith",
        "password": "abcdfghjkl"
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
        "password": "jane34678_23"
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
def test_user(client):
    payload =  {
        "username": "Jael",
        "password": "asdfghjkl",
        "email": "jael@test.com",
        "role": "user"
    }
    
    client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    return {"username": payload["username"], "password": payload["password"]}
    
@pytest.fixture()
def container(app):
    user_di = User_DI
    project_di = Project_DI
    task_id = Task_DI
    
    with app.app_context():
        user_di.register_user_dependencies()
        project_di.register_project_dependencies()
        task_id.register_task_dependencies()
    
    return {
        "user": user_di,
        "project": project_di,
        "task": task_id
    }
    