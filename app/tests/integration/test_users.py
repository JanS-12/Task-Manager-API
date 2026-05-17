from app.tests.utils.assertions import assert_error_response, assert_success_responses

""" Test Suite for User Route """

# ----- Admin Routes --------

    # ------ Success Routes ------
def test_admin_get_all_users(client, admin_auth_headers):
    response = client.get(
        "/api/v1/users/",
        headers = admin_auth_headers
    )
    print(response.get_json())

    assert_success_responses(response, 200, "Users Retrieved Successfully")
    
def test_admin_get_user(client, admin_auth_headers):  
    response = client.get(
        "/api/v1/users/1",
        headers = admin_auth_headers
    )
    assert_success_responses(response, 200, "User Retrieved Successfully") 
    
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
    
    assert_success_responses(response, 200, "User Updated Successfully") 
    
def test_admin_remove_user(client, test_user, admin_auth_headers):
    response = client.delete(
        "/api/v1/users/4",
        headers = admin_auth_headers
    )
    assert response.status_code == 204
    
    
# ----- Users Routes ---------

    # ------ Success Routes -------  
def test_user_protected_get_user(client, user_auth_headers):  
    response = client.get(
        "/api/v1/users/2",          # This means that there are 8 users on profile
        headers = user_auth_headers
    )
    assert_success_responses(response, 200, "User Retrieved Successfully")
    
    
    # ----- Failure, Unathorized, Forbidden Routes ----------    
def test_user_update_user_no_data(client, user_auth_headers):
    response = client.put(
        "/api/v1/users/2",
        json = "",
        headers = user_auth_headers
    )
    
    assert_error_response(response, 422, "ValidationError")
    
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
    
    assert_error_response(response, 422, "ValidationError")
    
def test_user_protected_route_no_token(client):
    response = client.get("/api/v1/users/2")

    assert response.status_code == 401
