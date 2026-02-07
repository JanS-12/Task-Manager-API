from app.repositories.task_repo import TaskRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.policies.task_policy import TaskPolicy
from app.utils.custom_exceptions import UserNotFound, TaskNotFound, ProjectNotFound

class RemoveTaskService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository, user_repo: UserRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.policy = TaskPolicy()
    
    def remove_task(self, project_id, task_id, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        
        project = self.project_repo.get_a_project(project_id)
        if not project:
            raise ProjectNotFound()
        
        task = self.task_repo.get_a_task(task_id)
        if not task:
            raise TaskNotFound()
        
        self.policy.belong_to_project(project, task)
        self.policy.can_delete_task(user, project)
        
        self.task_repo.remove_task(task_id)