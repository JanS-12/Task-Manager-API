
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
    
def test_user_remove_task(client, user_auth_headers):
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
def test_user_get_all_tasks_wrong_project(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/3/tasks/",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 403
    
def test_user_get_all_tasks_not_found_project(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/7/tasks/",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 404

    # --- Get a task
def test_user_get_a_task_project_not_found(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/5/tasks/3",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 404

def test_user_get_a_task_not_found(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/2/tasks/0",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 404    

def test_user_get_a_task_wrong_task(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/2/tasks/2",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 403
    
def test_user_get_a_task_wrong_project(client, user_auth_headers):
    response = client.get(
        "/api/v1/projects/1/tasks/3",
        headers = user_auth_headers
    )    
    
    assert response.status_code == 403

    # --- Create a Task 
def test_user_create_task_project_not_found(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "2"
    }   
    
    response = client.post(
        "/api/v1/projects/0/tasks/create",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 404
    
def test_user_create_task_no_data(client, user_auth_headers):
    response = client.post(
        "/api/v1/projects/2/tasks/create",
        json = "",
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

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
    
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "title" in data["message"]
    assert "project_id" in data["message"]
    
def test_user_create_task_wrong_project(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "1"
    }   
    
    response = client.post(
        "/api/v1/projects/1/tasks/create",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 403
    
    # ---- Update Task
def test_user_update_task_project_not_found(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "2"
    }   
    
    response = client.put(
        "/api/v1/projects/0/tasks/2",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 404
    
def test_user_update_task_no_data(client, user_auth_headers):
    response = client.put(
        "/api/v1/projects/2/tasks/7",
        json = "",
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

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
    
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert "title" in data["message"]
    assert "project_id" in data["message"]
    
def test_user_update_task_wrong_project(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "1"
    }   
    
    response = client.put(
        "/api/v1/projects/1/tasks/7",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 403

def test_user_update_task_not_found(client, user_auth_headers):
    payload = {
        "title": "User task test suite endpoint",
        "description": "Testing Endpoint for success",
        "project_id": "2"
    }   
    
    response = client.put(
        "/api/v1/projects/2/tasks/0",
        json = payload,
        headers = user_auth_headers
    ) 
    
    assert response.status_code == 404
    
    # Remove a task
def test_user_remove_task_project_not_found(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/0/tasks/1",
        headers = user_auth_headers
    )
    
    assert response.status_code == 404
    
def test_user_remove_task_not_found(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/2/tasks/0",
        headers = user_auth_headers
    )
    
    assert response.status_code == 404

def test_user_remove_task_wrong_task(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/2/tasks/1",
        headers = user_auth_headers
    )
    
    assert response.status_code == 403
    
def test_user_remove_task_wrong_project(client, user_auth_headers):
    response = client.delete(
        "/api/v1/projects/1/tasks/7",
        headers = user_auth_headers
    )
    
    assert response.status_code == 403