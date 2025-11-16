
""" Test Suite for Auth Routes """

# --- Success Routes ------
def test_create_user(client):
    payload = {
        "username": "Josue",
        "email": "josue@test.com",
        "password": "123456789",
        "role": "user"
    }

    response = client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "Josue"
    assert data["email"] == "josue@test.com"    
    
def test_login(client, test_user): 
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json = test_user, 
        content_type = "application/json"
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    
def test_user_refresh_access_token(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json = test_user, 
        content_type = "application/json"
    )
    
    assert response.status_code == 200
    token = response.get_json()["refresh_token"]
    header = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/api/v1/auth/refresh",
        headers = header
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    
    
# ------ Failure Routes --------
def test_registration_invalid_data(client):
    payload = {
        "username": "Jo",
        "email": "jo",
        "password": "12",
        "role": "user"
    }
    
    response = client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "username" in data["message"]
    assert "email" in data["message"]
    assert "password" in data["message"]
    
def test_registration_no_data(client):
    payload = {}
    
    response = client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data

def test_registration_duplicate_user(client):
    payload = {
        "username": "Duplicate",
        "email": "duplicate@test.com",
        "password": "asdfghjkl",
        "role": "user"
    }  
    
    client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    response = client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    assert response.status_code == 409
    data = response.get_json()
    assert "message" in data
    
def test_login_no_data(client):
    credentials = {}
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json = credentials, 
        content_type = "application/json"
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data
    
        
def test_login_invalid_password(client, test_user):
    credentials = {
        "username": test_user["username"],
        "password": "asdfg"
    }
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json = credentials, 
        content_type = "application/json"
    )
    
    assert response.status_code == 401
    data = response.get_json()
    assert "message" in data  

def test_login_invalid_username(client, test_user):
    credentials = {
        "username": "Manuela",
        "password": test_user["password"]
    }
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json = credentials, 
        content_type = "application/json"
    )
    
    assert response.status_code == 401
    data = response.get_json()
    assert "message" in data  
    
