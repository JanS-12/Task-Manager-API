import pytest 
from flask_jwt_extended import decode_token
from app.utils.custom_exceptions import (ExistingCredentialsError, 
InvalidCredentialsError, UserNotFound, AccessDenied)

def test_login_success(container):
    service = container.user.login_service        

    data = service.login("John Smith", "abcdfghjkl")
    
    assert "access_token" in data
    assert "refresh_token" in data    

    
def test_login_invalid_credentials(container):
    service = container.user.login_service.login
    
    with pytest.raises(InvalidCredentialsError):
        service("Joe", "1380u40")    


def test_logout_success(container):
    service = container.user
    
    data = service.login_service.login("John Smith", "abcdfghjkl")
    assert "access_token" in data
    assert "refresh_token" in data 
    
    service.logout_service.logout(1)
    
    access_jti = decode_token(data["access_token"])["jti"]
    refresh_jti = decode_token(data["refresh_token"])["jti"]
    
    expired_access_token = service.token_repository.get_revoked_token(access_jti)
    expired_refresh_token = service.token_repository.get_revoked_token(refresh_jti)
    
    assert expired_access_token.is_revoked()
    assert expired_refresh_token.is_revoked()
    
    
def test_logout_user_not_found(container):
    service = container.user.logout_service.logout
    
    with pytest.raises(UserNotFound):
        service(0)
            
        
def test_single_profile_success(container):
    service = container.user.user_profile_service.get
    
    user = service(2, 2)
    assert user is not None
    
    
def test_single_profile_user_not_found(container):
    service = container.user.user_profile_service.get
    
    with pytest.raises(UserNotFound):
        service(0, 2)
       
        
def test_single_profile_requester_not_found(container):
    service = container.user.user_profile_service.get
    
    with pytest.raises(UserNotFound):
        service(2, 0)
    

def test_multiple_profiles_success(container):
    service = container.user.users_profile_service.get
    
    users = service(1)
    assert users is not None


def test_multiple_profiles_admin_not_found(container):
    service = container.user.users_profile_service.get
    
    with pytest.raises(UserNotFound):
        service(0)

    
def test_multiple_profiles_not_admin(container):
    service = container.user.users_profile_service.get
    
    with pytest.raises(AccessDenied):
        service(2)
        
#NOTE: Can't test if there no users, since there must be at least one admin.

def test_registration_success(container):
    service = container.user.registration_service
    
    payload = {
        "username": "Julian",
        "password": "asdertoqf",
        "email": "julian@test.com",
        "role": "user"
    }
    
    user = service.create_profile(payload)
    assert user is not None
    
    
def test_registration_existing_credentials(container):
    service = container.user.registration_service
    
    payload = {
        "username": "John Smith",
        "password": "asdertoqf",
        "email": "john@test.com",
        "role": "user"
    }
    
    with pytest.raises(ExistingCredentialsError):
        service.create_profile(payload)
        
        
def test_update_user_success(container):
    service = container.user.update_service
    
    payload = {
        "email": "testing@testing.com"
    }
    
    user = service.update(2, 2, payload)
    assert user is not None
    
    
def test_update_user_not_found(container):
    service = container.user.update_service.update
    payload = {
        "email": "testing@testing.com"
    }
    
    with pytest.raises(UserNotFound):
        service(0, 2, payload)
        
        
def test_update_requester_not_found(container):
    service = container.user.update_service.update
    payload = {
        "email": "testing@testing.com"
    }
    
    with pytest.raises(UserNotFound):
        service(2, 0, payload)
        
        
def test_update_user_access_denied(container):
    service = container.user.update_service.update
    payload = {
        "email": "testing@testing.com"
    }
    
    with pytest.raises(AccessDenied):
        service(1, 2, payload)   
    
    
def test_refresh_access_token_success(container):
    service = container.user        

    data = service.login_service.login("John Smith", "abcdfghjkl")
    
    assert "access_token" in data
    assert "refresh_token" in data
    
    new_access_token = service.refresh_access_token_service.refresh_access_token(1)
    assert data["access_token"] != new_access_token
    
    
def test_remove_user_success(container):
    service = container.user
    
    service.remove_service.remove(2, 1)
    assert service.user_repository.get_by_id(2) is None
    
    
def test_remove_user_not_found(container):
    service = container.user.remove_service.remove
    
    with pytest.raises(UserNotFound):
        service(0, 1)
    
    
def test_remove_requester_not_found(container):
    service = container.user.remove_service.remove
    
    with pytest.raises(UserNotFound):
        service(2, 0)   
    
    
def test_remove_user_access_denied(container):
    service = container.user.remove_service.remove
    
    with pytest.raises(AccessDenied):
        service(2, 2)
        
        
def test_remove_requester_access_denied(container):
    service = container.user.remove_service.remove
    
    with pytest.raises(AccessDenied):
        service(2, 3)