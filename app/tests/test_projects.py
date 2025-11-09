
""" Test Suite for Projects """

# ---- Admin Routes ----
    # --- Success Routes ---
def test_admin_get_all_projects(client, admin_auth_headers):
    response = client.get(
        "/api/v1/projects/",
        headers = admin_auth_headers
    )    

    assert response.status_code == 200

def test_admin_get_a_project(client, admin_auth_headers):
    response = client.get(
        "/api/v1/projects/1",
        headers = admin_auth_headers
    )    
    
    assert response.status_code == 200 

def test_admin_create_a_project(client, admin_auth_headers):
    payload = {
        "title": "Project Test Suite",
        "description": "Testing the endpoint from test suite.",
        "owner_id": "1"
    }
    
    response = client.post(
        "/api/v1/projects/register",
        json = payload,
        headers = admin_auth_headers
    )

    assert response.status_code == 201    
    data = response.get_json()
    assert "id" in data

def test_admin_update_project(client, admin_auth_headers):
    payload = {
        "title": "Project Test Suite",
        "description": "Testing the update endpoint from test suite.",
        "owner_id": "1"
    }
    
    response = client.put(
        "/api/v1/projects/4",
        json = payload,
        headers = admin_auth_headers
    )

    assert response.status_code == 200   
    data = response.get_json()
    assert "id" in data
    
# Test Admin Delete Works, yet we are not testing it because it would
#   fail following tests in the suite

# ---- User Routes ----
    # --- Success Routes ---
def test_user_get_user_projects(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 200
    
def test_user_get_a_user_project(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/2",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data 

def test_user_create_project(client, user_auth_headers):
    payload = {
        "title": "Project Test Suite of User",
        "description": "Testing the endpoint from test suite of user.",
        "owner_id": "2"
    }
    
    response = client.post(
        "/api/v1/projects/register",
        json = payload,
        headers = user_auth_headers
    )

    assert response.status_code == 201    
    data = response.get_json()
    assert "id" in data


       
def test_user_update_project(client, user_auth_headers):
    payload = {
        "title": "Project Test Suite User",
        "description": "Testing the update user endpoint from test suite.",
        "owner_id": "2"
    }
    
    response = client.put(
        "/api/v1/projects/5",
        json = payload,
        headers = user_auth_headers
    )

    assert response.status_code == 200   
    data = response.get_json()
    assert "id" in data

def test_user_delete_project(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/5", 
        headers = user_auth_headers
    )
    
    assert response.status_code == 204
    
    
    # --- Failure Routes ---
def test_user_get_wrong_project(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/1",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 403
    data = response.get_json()
    assert "error" in data
    
def test_user_create_project_no_data(client, user_auth_headers):
    response = client.post(
        "/api/v1/projects/register",
        json = "",
        headers = user_auth_headers
    )

    assert response.status_code == 400    
    data = response.get_json()
    assert "error" in data

def test_user_create_project_invalid_data(client, user_auth_headers):
    payload = {
        "title": "r",
        "description": "",
        "owner_id": "."
    }
    
    response = client.post(
        "/api/v1/projects/register",
        json = payload,
        headers = user_auth_headers
    )

    assert response.status_code == 422    
    data = response.get_json()
    assert "error" in data
    assert "title" in data["message"]
    assert "owner_id" in data["message"]     

def test_user_update_wrong_project(client, user_auth_headers):
    payload = {
        "title": "Project Test Suite User",
        "description": "Testing the update user endpoint from test suite.",
        "owner_id": "2"
    }
    
    response = client.put(
        "/api/v1/projects/4",
        json = payload,
        headers = user_auth_headers
    )

    assert response.status_code == 403   
    data = response.get_json()
    assert "error" in data

def test_user_update_project_no_data(client, user_auth_headers):
    response = client.post(
        "/api/v1/projects/register",
        json = "",
        headers = user_auth_headers
    )

    assert response.status_code == 400    
    data = response.get_json()
    assert "error" in data

def test_user_update_project_invalid_data(client, user_auth_headers):
    payload = {
        "title": "r",
        "description": "",
        "owner_id": "."
    }
    
    response = client.put(
        "/api/v1/projects/5",
        json = payload,
        headers = user_auth_headers
    )

    assert response.status_code == 422    
    data = response.get_json()
    assert "error" in data
    assert "title" in data["message"]
    assert "owner_id" in data["message"]
    
def test_user_delete_wrong_project(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/4", 
        headers = user_auth_headers
    )
    
    assert response.status_code == 403

def test_user_delete_not_found(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/5", 
        headers = user_auth_headers
    )
    
    assert response.status_code == 404