from app.services.tasks.retrieve import GetTaskService, GetTasksService
from app.services.tasks.create import CreateTaskService
from app.services.tasks.modify import UpdateTaskService
from app.services.tasks.remove import RemoveTaskService

from app.controllers.tasks.retrieve import GetTaskController, GetTasksController
from app.controllers.tasks.create import CreateTaskController
from app.controllers.tasks.modify import UpdateTaskController
from app.controllers.tasks.remove import RemoveTaskController

from app.repositories.project_repo import ProjectRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.user_repo import UserRepository

class TaskContainer:
    def __init__(
        self, 
        user_repository=None,
        project_repository=None,
        task_repository=None
    ):
        # Dependencies 
        self.user_repository = user_repository or UserRepository()
        self.project_repository = project_repository or ProjectRepository()
        self.task_repository = task_repository or TaskRepository()
        
        # Services
        self.retrieve_task_service = GetTaskService(self.project_repository, self.user_repository, self.task_repository)        
        self.retrieve_tasks_service = GetTasksService(self.project_repository, self.user_repository, self.task_repository)    
        self.create_service = CreateTaskService(self.project_repository, self.user_repository, self.task_repository)
        self.update_service = UpdateTaskService(self.project_repository, self.user_repository, self.task_repository)
        self.remove_service = RemoveTaskService(self.project_repository, self.user_repository, self.task_repository)
        
        # Controllers
        self.retrieve_task_controller = GetTaskController(self.retrieve_task_service)
        self.retrieve_tasks_controller = GetTasksController(self.retrieve_tasks_service)
        self.create_controller = CreateTaskController(self.create_service)
        self.update_controller = UpdateTaskController(self.update_service)
        self.remove_controller = RemoveTaskController(self.remove_service)