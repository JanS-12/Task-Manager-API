from app.models.user import User

""" Test Suite for User Route """

# ----- Admin Routes --------

    # ------ Success Routes ------
def test_admin_get_all_users(client, admin_auth_headers):
    response = client.get(
        "/api/v1/users/",
        headers = admin_auth_headers
    )

    assert response.status_code == 200 
    
def test_admin_get_user(client, admin_auth_headers):  
    response = client.get(
        "/api/v1/users/1",
        headers = admin_auth_headers
    )
    assert response.status_code == 200  
    
def test_admin_update_user(client, test_user, admin_auth_headers):    
    payload = { # User created in test_auth
        "username": "Junior",
        "email": "junior@test.com",
        "password": "123456789",
        "role": "user"
    }
    
    response = client.put(
        "/api/v1/users/4", 
        json = payload,
        headers = admin_auth_headers
    )
    
    assert response.status_code == 200
    
def test_admin_user_delete(client, test_user, admin_auth_headers):
    response = client.delete(
        "/api/v1/users/4",
        headers = admin_auth_headers
    )
    
    assert response.status_code == 204
    
    # ----- Failure Routes --------
def test_admin_get_user_not_found(client, admin_auth_headers):  
    response = client.get(
        "/api/v1/users/0",
        headers = admin_auth_headers
    )
    
    assert response.status_code == 404
    
def test_admin_delete_user_not_found(client, admin_auth_headers):
    response = client.delete(
        "/api/v1/users/0",
        headers = admin_auth_headers
    )
    
    assert response.status_code == 404
    
        
    
# ----- Users Routes ---------

    # ------ Success Routes -------  
def test_user_get_user(client, user_auth_headers):  
    response = client.get(
        "/api/v1/users/2",          # This means that there are 8 users on profile
        headers = user_auth_headers
    )
    assert response.status_code == 200 
    
def test_user_logout(client, user_auth_headers):
    response = client.post(
        "/api/v1/auth/logout",
        headers = user_auth_headers
    )
    
    assert response.status_code == 200
    
    
    # ----- Failure, Unathorized, Forbidden Routes ----------
def test_user_get_all_users(client, user_auth_headers):
    response = client.get(
        "/api/v1/users/",
        headers = user_auth_headers
    )
    assert response.status_code == 403
    
def test_user_get_wrong_user(client, user_auth_headers):  
    response = client.get(
        "/api/v1/users/1",
        headers = user_auth_headers
    )
    assert response.status_code == 403  
    
def test_user_update_user_no_data(client, user_auth_headers):
    response = client.put(
        "/api/v1/users/2",
        json = "",
        headers = user_auth_headers
    )
    
    assert response.status_code == 400  
    data = response.get_json()
    assert "error" in data
    
def test_user_update_user_invalid_data(client, user_auth_headers):
    payload = {
        "username": "Sl",
        "email": "samu",
        "password": "45",
        "role": ""
    }  
    
    response = client.put(
        "/api/v1/users/2",
        json = payload,
        headers = user_auth_headers
    )
    
    assert response.status_code == 422  
    data = response.get_json()
    assert "error" in data 
    assert "username" in data["message"]
    assert "password" in data["message"]
    assert "email" in data["message"]

def test_user_update_user_not_found(client, user_auth_headers):
    payload = {
        "username": "Samuel",
        "email": "samuel@test.com",
        "password": "aurora12345",
        "role": "user"
    }    
    
    response = client.put(
        "/api/v1/users/0",
        json = payload,
        headers = user_auth_headers
    )
    
    assert response.status_code == 404

def test_user_update_wrong_user(client, user_auth_headers):
    payload = {
        "username": "Samuel",
        "email": "samuel@test.com",
        "password": "aurora12345",
        "role": "user"
    }    
    
    response = client.put(
        "/api/v1/users/1",
        json = payload,
        headers = user_auth_headers
    )
    
    assert response.status_code == 403    
    
def test_user_delete_user(client, user_auth_headers):
    response = client.delete(
        "/api/v1/users/3",
        headers = user_auth_headers
    )
    
    assert response.status_code == 403
    data = response.get_json() 
    assert "message" in data
    