from app.tests.utils.assertions import assert_error_response
"""  Test Suite for Tasks """

# ---- Admin Routes -----
    # ---- Success Routes -----
def test_admin_get_all_tasks(client, admin_auth_headers):
    response = client.get(
        "/api/v1/projects/2/tasks/",
        headers = admin_auth_headers
    )     
       
    assert response.status_code == 200
   
def test_admin_get_a_task(client, admin_auth_headers):
    response = client.get(
        "/api/v1/projects/1/tasks/1",
        headers = admin_auth_headers
    )    

    assert response.status_code == 200

def test_admin_create_task(client, admin_auth_headers):
    payload = {     # Task #7 under Project #1
        "title": "Admin task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "1"
    }   
    
    response = client.post(
        "/api/v1/projects/1/tasks/create",
        json = payload,
        headers = admin_auth_headers
    ) 
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data

def test_admin_update_task(client, admin_auth_headers):
    payload = {     # Task #7 under Project #1
        "title": "Admin task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "1"
    }   
    
    response = client.post(
        "/api/v1/projects/1/tasks/create",
        json = payload,
        headers = admin_auth_headers
    ) 
    
    assert response.status_code == 201
    
    payload = {
        "title": "Admin update task test suite endpoint",
        "description": "Testing Endpoint for update success",
        "project_id": "1"
    }   
    
    response = client.put(
        "/api/v1/projects/1/tasks/7",
        json = payload,
        headers = admin_auth_headers
    ) 
    
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    
def test_admin_delete_task(client, admin_auth_headers):
    payload = {     # Task #7 under Project #1
        "title": "Admin task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "1"
    }   
    
    response = client.post(
        "/api/v1/projects/1/tasks/create",
        json = payload,
        headers = admin_auth_headers
    ) 
    
    assert response.status_code == 201
    
    response = client.delete(
        "/api/v1/projects/1/tasks/7",
        headers = admin_auth_headers
    )
    
    # Now there should be the original 6 seeded tasks
    assert response.status_code == 204

# ---- User Routes ----
    # --- Success Routes ---
def test_user_get_all_tasks(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/2/tasks/",
        headers = user_auth_headers
    )    
    
    count = len(response.get_json())
    
    assert response.status_code == 200
    assert count == 2
    
def test_user_get_a_task(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/2/tasks/3",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 200
    
def test_user_create_task(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "2"
    }   
    
    response = client.post(
        "/api/v1/projects/2/tasks/create",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    
def test_user_update_task(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "2"
    }   
    
    response = client.post(
        "/api/v1/projects/2/tasks/create",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 201
    
    payload = {
        "title": "User update task test suite endpoint",
        "description": "Testing Endpoint for update success",
        "project_id": "2"
    }   
    
    response = client.put(
        "/api/v1/projects/2/tasks/7",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    
def test_user_delete_task(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "2"
    }   
    
    response = client.post(
        "/api/v1/projects/2/tasks/create",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 201
    
    response = client.delete(
        "/api/v1/projects/2/tasks/7",
        headers = user_auth_headers
    )
    
    assert response.status_code == 204
    
    # --- Failure Routes ---    
def test_user_protected_route_no_token(client):
    response = client.get("/api/v1/projects/2/tasks/")

    assert response.status_code == 401
    
def test_user_create_task_no_data(client, user_auth_headers):
    response = client.post(
        "/api/v1/projects/2/tasks/create",
        json = "",
        headers = user_auth_headers
    ) 
    
    assert_error_response(response, 400, "NoDataError")

def test_user_create_task_invalid_data(client, user_auth_headers):
    payload = {
        "title": "t",
        "description": "",
        "project_id": ""
    }
    
    response = client.post(
        "/api/v1/projects/2/tasks/create",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert_error_response(response, 422, "ValidationError")
    
    # ---- Update Task
def test_user_update_task_no_data(client, user_auth_headers):
    response = client.put(
        "/api/v1/projects/2/tasks/7",
        json = "",
        headers = user_auth_headers
    ) 
    
    assert_error_response(response, 400, "NoDataError")

def test_user_update_task_invalid_data(client, user_auth_headers):
    payload = {
        "title": "t",
        "description": "",
        "project_id": ""
    }
    
    response = client.put(
        "/api/v1/projects/2/tasks/3",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert_error_response(response, 422, "ValidationError")