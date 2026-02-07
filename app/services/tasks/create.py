from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.repositories.task_repo import TaskRepository

from app.utils.custom_exceptions import UserNotFound, TaskNotFound, ProjectNotFound
from app.policies.task_policy import TaskPolicy

class CreateTaskService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.task_repo = task_repo
        self.policy = TaskPolicy()
        pass
    
    def create_task(self, data, project_id, requester_id):
        requester = self.user_repo.get_by_id(requester_id)
        if not requester:
            raise UserNotFound()
        
        project = self.project_repo.get_a_project(project_id)
        if not project:
            raise ProjectNotFound()
        
        self.policy.can_create_task(requester, project)
        task = self.task_repo.create_task(project.id, data)
        return task
        
        