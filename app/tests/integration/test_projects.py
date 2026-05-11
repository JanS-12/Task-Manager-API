from app.tests.utils.assertions import assert_error_response, assert_success_responses
""" Test Suite for Projects """

# ---- Admin Routes ----
    # --- Success Routes ---
def test_admin_get_all_projects(client, admin_auth_headers):
    response = client.get(
        "/api/v1/projects/",
        headers = admin_auth_headers
    )    
    assert_success_responses(response, 200, "Projects retrieved successfully") 

def test_admin_get_a_project(client, admin_auth_headers):
    response = client.get(
        "/api/v1/projects/1",
        headers = admin_auth_headers
    )    
    
    assert_success_responses(response, 200, "Project retrieved successfully") 


def test_admin_create_project(client, admin_auth_headers):  
    payload = {     
        "title": "Project Test Suite",
        "description": "Testing the endpoint from test suite.",
        "owner_id": "1"
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = admin_auth_headers
    )

    assert_success_responses(response, 201, "Project created successfully")


def test_admin_update_project(client, admin_auth_headers):
    payload = {     # This would be project #4
        "title": "Project Test Suite",
        "description": "Testing the endpoint from test suite.",
        "owner_id": "1"
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = admin_auth_headers
    )

    assert_success_responses(response, 201, "Project created successfully") 
    
    payload = {
        "title": "Project Test Suite",
        "description": "Testing the update endpoint from test suite.",
        "owner_id": "1"
    }
    
    response = client.put(
        "/api/v1/projects/4",   # Project #4
        json = payload,
        headers = admin_auth_headers
    )

    assert_success_responses(response, 200, "Project updated successfully")

    
def test_admin_delete_project(client, admin_auth_headers):
    payload = {     # This would be project #4
        "title": "Project Test Suite",
        "description": "Testing the endpoint from test suite.",
        "owner_id": "1"
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = admin_auth_headers
    )

    assert_success_responses(response, 201, "Project created successfully") 
    
    response = client.delete(
        "/api/v1/projects/4", # Project #4
        headers = admin_auth_headers
    )
    
    # Now, there should be the three seeded initial projects
    assert response.status_code == 204


# ---- User Routes ----
    # --- Success Routes ---
def test_user_get_user_projects(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/",
        headers = user_auth_headers
    )    
    
    assert_success_responses(response, 200, "Projects retrieved successfully")
    
    
def test_user_get_a_user_project(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/2",
        headers = user_auth_headers
    )    
    
    assert_success_responses(response, 200, "Project retrieved successfully")


def test_user_create_project(client, user_auth_headers):
    payload = {
        "title": "Project Test Suite of User",
        "description": "Testing the endpoint from test suite of user.",
        "owner_id": "2"
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = user_auth_headers
    )

    assert_success_responses(response, 201, "Project created successfully")
    
       
def test_user_update_project(client, user_auth_headers):
    payload = { # Project #4
        "title": "Project Test Suite of User",
        "description": "Testing the endpoint from test suite of user.",
        "owner_id": "2"
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = user_auth_headers
    )
    
    assert_success_responses(response, 201, "Project created successfully")
    
    payload = {
        "title": "Project Test Suite User",
        "description": "Testing the update user endpoint from test suite.",
        "owner_id": "2"
    }
    
    response = client.put(  # Project #4
        "/api/v1/projects/4",
        json = payload,
        headers = user_auth_headers
    )

    assert_success_responses(response, 200, "Project updated successfully")


def test_user_delete_project(client, user_auth_headers):
    payload = { # Project #4
        "title": "Project Test Suite of User",
        "description": "Testing the endpoint from test suite of user.",
        "owner_id": "2"
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = user_auth_headers
    )
    
    assert_success_responses(response, 201, "Project created successfully")
    
    response = client.delete(
        "/api/v1/projects/4", # Project #4
        headers = user_auth_headers
    )
    
    assert response.status_code == 204
    
    
    # --- Failure Routes ---        
def test_user_protected_route_no_token(client):
    response = client.get("/api/v1/projects/2")
    
    assert response.status_code == 401
    
def test_user_create_project_no_data(client, user_auth_headers):
    response = client.post(
        "/api/v1/projects/create",
        json = "",
        headers = user_auth_headers
    )

    assert_error_response(response, 400, "NoDataError")


def test_user_create_project_invalid_data(client, user_auth_headers):
    payload = {
        "title": "r",
        "description": "",
        "owner_id": "."
    }
    
    response = client.post(
        "/api/v1/projects/create",
        json = payload,
        headers = user_auth_headers
    )

    assert_error_response(response, 422, "ValidationError")


def test_user_update_project_no_data(client, user_auth_headers):
    response = client.put(
        "/api/v1/projects/2",
        json = "",
        headers = user_auth_headers
    )

    assert_error_response(response, 400, "NoDataError")


def test_user_update_project_invalid_data(client, user_auth_headers):
    payload = {
        "title": "r",
        "description": "",
        "owner_id": "."
    }
    
    response = client.put(
        "/api/v1/projects/2",
        json = payload,
        headers = user_auth_headers
    )

    assert_error_response(response, 422, "ValidationError")
    