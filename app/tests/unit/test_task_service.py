import pytest 

from app.utils.custom_exceptions import (UserNotFound, AccessDenied, TaskIncorrectProject, TaskNotFound, ProjectNotFound)

def test_task_creation_success(container):
    service = container.task.create_service
    
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    task = service.create_task(payload, 2, 2)
    assert task is not None
    
    
def test_task_creation_user_not_found(container):
    service = container.task.create_service.create_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(UserNotFound):
        service(payload, 2, 0)
        
        
def test_task_creation_project_not_found(container):
    service = container.task.create_service.create_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(ProjectNotFound):
        service(payload, 0, 2)
        

def test_task_creation_access_denied(container):
    service = container.task.create_service.create_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(AccessDenied):
        service(payload, 1, 2)
        
        
def test_task_update_success(container):
    service = container.task.update_service
    
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    task = service.update_task(payload, 2, 3, 2)
    assert task is not None
    
    
def test_task_update_user_not_found(container):
    service = container.task.update_service.update_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(UserNotFound):
        service(payload, 2, 3, 0)
        
        
def test_task_update_project_not_found(container):
    service = container.task.update_service.update_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(ProjectNotFound):
        service(payload, 0, 3, 2)
        
        
def test_task_update_task_not_found(container):
    service = container.task.update_service.update_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(TaskNotFound):
        service(payload, 2, 0, 2)
        

def test_task_update_access_denied(container):
    service = container.task.update_service.update_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(AccessDenied):
        service(payload, 2, 3, 3)
        

def test_task_update_incorrect_project(container):
    service = container.task.update_service.update_task
    payload = {
        "title": "Task Unit Testing",
        "description": "Unit Testing task"
    }
    
    with pytest.raises(TaskIncorrectProject):
        service(payload, 1, 3, 2)
        
        
def test_task_retrieve_success(container):
    service = container.task.retrieve_task_service
    
    task = service.get_task(2, 3, 2)
    assert task is not None
    

def test_task_retrieve_user_not_found(container):
    service = container.task.retrieve_task_service.get_task
    
    with pytest.raises(UserNotFound):
        service(2, 3, 0)
        
        
def test_task_retrieve_project_not_found(container):
    service = container.task.retrieve_task_service.get_task
    
    with pytest.raises(ProjectNotFound):
        service(0, 3, 2)
        
        
def test_task_retrieve_task_not_found(container):
    service = container.task.retrieve_task_service.get_task
    
    with pytest.raises(TaskNotFound):
        service(2, 0, 2)
        

def test_task_retrieve_access_denied(container):
    service = container.task.retrieve_task_service.get_task
    
    with pytest.raises(AccessDenied):
        service(2, 3, 3)
        

def test_task_retrieve_incorrect_project(container):
    service = container.task.retrieve_task_service.get_task
    
    with pytest.raises(TaskIncorrectProject):
        service(1, 3, 2)
        
        
def test_tasks_retrieve_success(container):
    service = container.task.retrieve_tasks_service
    
    task = service.get_tasks(2, 2)
    assert task is not None
    

def test_tasks_retrieve_user_not_found(container):
    service = container.task.retrieve_tasks_service.get_tasks
    
    with pytest.raises(UserNotFound):
        service(2, 0)
        
        
def test_tasks_retrieve_project_not_found(container):
    service = container.task.retrieve_tasks_service.get_tasks
    
    with pytest.raises(ProjectNotFound):
        service(0, 2)
        
        
def test_tasks_retrieve_task_not_found(container):
    service = container.project.create_service
    
    payload = {
        "title": "unit testing",
        "description": "Testing testing testing"
    }
    
    project = service.create_project(payload, 2)
    
    service = container.task.retrieve_tasks_service.get_tasks
    
    with pytest.raises(TaskNotFound):
        service(4, 2)
        

def test_tasks_retrieve_access_denied(container):
    service = container.task.retrieve_tasks_service.get_tasks
    
    with pytest.raises(AccessDenied):
        service(2, 3)
        
        
def test_task_remove_success(container):
    service = container.task.remove_service.remove_task
    service(2, 3, 2)    
    
    assert container.task.task_repository.get_a_task(3) is None
    
    
def test_task_remove_user_not_found(container):
    service = container.task.remove_service.remove_task
    
    with pytest.raises(UserNotFound):
        service(2, 3, 0)
        
        
def test_task_remove_project_not_found(container):
    service = container.task.remove_service.remove_task
    
    with pytest.raises(ProjectNotFound):
        service(0, 3, 2)
        
        
def test_task_remove_task_not_found(container):
    service = container.task.remove_service.remove_task
    
    with pytest.raises(TaskNotFound):
        service(2, 0, 2)
        

def test_task_remove_access_denied(container):
    service = container.task.remove_service.remove_task
    
    with pytest.raises(AccessDenied):
        service(2, 3, 3)
        

def test_task_remove_incorrect_project(container):
    service = container.task.remove_service.remove_task
    
    with pytest.raises(TaskIncorrectProject):
        service(1, 3, 2)
    