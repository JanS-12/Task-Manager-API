import pytest 
from app.utils.custom_exceptions import (UserNotFound, ProjectNotFound, AccessDenied)

def test_project_creation_success(container):
    service = container.project.create_service
    
    payload = {
        "title": "unit testing",
        "description": "Testing testing testing"
    }
    
    project = service.create_project(payload, 2)
    assert project is not None
    
    
def test_project_creation_user_not_found(container):
    service = container.project.create_service.create_project
    payload = {
        "title": "unit testing",
        "description": "Testing testing testing"
    }
    
    with pytest.raises(UserNotFound):
        service(payload, 0)
        

def test_get_single_project_success(container):
    service = container.project.retrieve_project_service
    
    project = service.get_project(1, 1)
    assert project is not None
    
    
def test_get_single_project_not_found(container):
    service = container.project.retrieve_project_service.get_project
    
    with pytest.raises(ProjectNotFound):
        service(0, 1)
        
        
def test_get_single_project_user_not_found(container):
    service = container.project.retrieve_project_service.get_project
    
    with pytest.raises(UserNotFound):
        service(1, 0)
        

def test_get_single_project_access_denied(container):
    service = container.project.retrieve_project_service.get_project
    
    with pytest.raises(AccessDenied):
        service(1, 2)
        
        
def test_get_projects_user_success(container):
    service = container.project.retrieve_projects_service
    
    projects = service.get_projects(2)
    assert projects is not None
    

def test_get_projects_admin_success(container):
    service = container.project.retrieve_projects_service
    
    projects = service.get_projects(1)
    assert projects is not None
    
    
def test_get_projects_user_not_found(container):
    service = container.project.retrieve_projects_service.get_projects
    
    with pytest.raises(UserNotFound):
        service(0)
        

def test_get_projects_project_not_found(container):
    service = container.user
    
    payload = {
        "username": "Julian",
        "password": "asdertoqf",
        "email": "julian@test.com",
        "role": "user"
    }
    
    user = service.registration_service.create_profile(payload)
    data = service.login_service.login("Julian", "asdertoqf")
    
    service = container.project.retrieve_projects_service.get_projects
    
    with pytest.raises(ProjectNotFound):
        service(4)
        

def test_update_project_success(container):
    service = container.project.update_service
    
    payload = {
        "title": "unit testing update",
        "description": "unit testing update testing"
    }
    
    project = service.update_project(payload, 2, 2)
    assert project is not None
    

def test_update_project_user_not_found(container):
    service = container.project.update_service.update_project
    
    payload = {
        "title": "unit testing update",
        "description": "unit testing update testing"
    }
    
    with pytest.raises(UserNotFound):
        service(payload, 2, 0)
        

def test_update_project_project_not_found(container):
    service = container.project.update_service.update_project
    
    payload = {
        "title": "unit testing update",
        "description": "unit testing update testing"
    }
    
    with pytest.raises(ProjectNotFound):
        service(payload, 0, 2)
        
        
def test_update_project_access_denied(container):
    service = container.project.update_service.update_project
    
    payload = {
        "title": "unit testing update",
        "description": "unit testing update testing"
    }
    
    with pytest.raises(AccessDenied):
        service(payload, 1, 2)
        
        
def test_remove_project_success(container):
    service = container.project
    
    service.remove_service.remove_project(1, 1)
    assert service.project_repository.get_a_project(1) is None
    
    
def test_remove_project_user_not_found(container):
    service = container.project.remove_service.remove_project
    
    with pytest.raises(UserNotFound):
        service(2, 0)
        

def test_remove_project_project_not_found(container):
    service = container.project.remove_service.remove_project
    
    with pytest.raises(ProjectNotFound):
        service(0, 2)
        
        
def test_remove_project_access_denied(container):
    service = container.project.remove_service.remove_project
    
    with pytest.raises(AccessDenied):
        service(1, 2)