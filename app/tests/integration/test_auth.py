from app.tests.utils.assertions import assert_error_response, assert_success_responses
""" Test Suite for Auth Routes """

# --- Success Routes ------
def test_registration(client):
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
    
    assert_success_responses(response, 201, "Registration Successful")  
    
def test_login(client, test_user): 
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json = test_user, 
        content_type = "application/json"
    )
    
    assert_success_responses(response, 200, "Login Successful")
    
    
def test_logout(client, user_auth_headers):
    response = client.post(
        "/api/v1/auth/logout",
        headers = user_auth_headers
    )

    assert_success_responses(response, 200, "Logout Successful")
    
    
def test_user_refresh_access_token(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json = test_user, 
        content_type = "application/json"
    )
    
    assert response.status_code == 200
    token = response.get_json()["success"]["data"]["refresh_token"]
    header = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/api/v1/auth/refresh",
        headers = header
    )
    
    assert_success_responses(response, 200, "New Access Token Issued")
    
    
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
    
    assert_error_response(response, 422, "ValidationError")
    
    
def test_registration_no_data(client):
    payload = {}
    
    response = client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    assert_error_response(response, 400, "NoDataError")

def test_registration_duplicate_user(client):
    payload = {
        "username": "Manuel Garcia",
        "email": "garcia0823@test.com",
        "password": "nicole_234891$",
        "role": "user"
    }  
    
    response = client.post(
        "/api/v1/auth/register",
        json = payload, 
        content_type = "application/json"
    )
    
    assert_error_response(response, 409, "ExistingCredentialsError")
    
def test_login_no_data(client):
    credentials = {}
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json = credentials, 
        content_type = "application/json"
    )
    
    assert_error_response(response, 400, "NoDataError")
    
        
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
    
    assert_error_response(response, 401, "InvalidCredentialsError")


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
    
    assert_error_response(response, 401, "InvalidCredentialsError") 
    
