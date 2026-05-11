
def assert_error_response(response, status_code, error_type):
    data = response.get_json()
    
    assert response.status_code == status_code
    assert data["error"]["type"] == error_type
    assert "message" in data["error"]
    assert "timestamp" in data["error"]
    
    
def assert_success_responses(response, status_code, message):
    data = response.get_json()
    
    assert "success" in data
    assert response.status_code == status_code
    assert data["success"]["message"] == message
    assert "data" in data["success"]
    assert "timestamp" in data["success"]