from app.services.tasks.create import CreateTaskService
from app.services.tasks.retrieve import GetTaskService, GetTasksService
from app.services.tasks.modify import UpdateTaskService
from app.services.tasks.remove import RemoveTaskService

from app.controllers.tasks.create import CreateTaskController
from app.controllers.tasks.retrieve import GetTaskController, GetTasksController
from app.controllers.tasks.modify import UpdateTaskController
from app.controllers.tasks.remove import RemoveTaskController

from app.repositories.project_repo import ProjectRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.user_repo import UserRepository

class Task_DI:
    user_repository = None
    project_repository = None
    task_repository = None
    
    retrieve_task_service = None
    retrieve_task_controller = None
    
    retrieve_tasks_service = None
    retrieve_tasks_controller = None
    
    create_task_service = None
    create_task_controller = None
    
    update_task_service = None
    update_task_controller = None
    
    remove_task_service = None
    remove_task_controller = None
    
    def register_task_dependencies():
        Task_DI.user_repository = UserRepository()
        Task_DI.project_repository = ProjectRepository()
        Task_DI.task_repository = TaskRepository()
        
        Task_DI.create_task_service = CreateTaskService(Task_DI.project_repository, Task_DI.user_repository, Task_DI.task_repository)
        Task_DI.create_task_controller = CreateTaskController(Task_DI.create_task_service)
        
        Task_DI.retrieve_task_service = GetTaskService(Task_DI.project_repository, Task_DI.user_repository, Task_DI.task_repository)
        Task_DI.retrieve_task_controller = GetTaskController(Task_DI.retrieve_task_service)
        
        Task_DI.retrieve_tasks_service = GetTasksService(Task_DI.project_repository, Task_DI.user_repository, Task_DI.task_repository)
        Task_DI.retrieve_tasks_controller = GetTasksController(Task_DI.retrieve_tasks_service)
        
        Task_DI.update_task_service = UpdateTaskService(Task_DI.project_repository, Task_DI.task_repository, Task_DI.user_repository)
        Task_DI.update_task_controller = UpdateTaskController(Task_DI.update_task_service)
        
        Task_DI.remove_task_service = RemoveTaskService(Task_DI.project_repository, Task_DI.task_repository, Task_DI.user_repository)
        Task_DI.remove_task_controller = RemoveTaskController(Task_DI.remove_task_service)