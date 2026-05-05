import pytest 

from app.utils.custom_exceptions import InvalidCredentialsError

def test_login_success(container):
    service = container["user"].login_service
        
    data = service.login("John Smith", "abcdfghjkl")
    assert "access_token" in data
    assert "refresh_token" in data
    
    
def test_login_invalid_credentials(container):
    service = container["user"].login_service
    
    with pytest.raises(InvalidCredentialsError):
        data = service.login("Joe", "1380u40")    