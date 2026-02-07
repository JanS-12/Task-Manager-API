from app.repositories.task_repo import TaskRepository
from app.repositories.project_repo import ProjectRepository   
from app.repositories.user_repo import UserRepository
from app.policies.task_policy import TaskPolicy
from app.utils.custom_exceptions import UserNotFound, TaskNotFound, ProjectNotFound

class GetTaskService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.task_repo = task_repo
        self.policy = TaskPolicy()
        
    def get_task(self, project_id, task_id, user_id):
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
        self.policy.can_view_task(user, project)
        
        return task
    
class GetTasksService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.task_repo = task_repo
        self.policy = TaskPolicy()
        
    def get_tasks(self, project_id, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        
        project = self.project_repo.get_a_project(project_id)
        if not project:
            raise ProjectNotFound()
        
        if self.policy.can_view_all_tasks(user):
            tasks = self.task_repo.get_all_tasks()
        else:
            self.policy.can_view_task(user, project)
            tasks = self.task_repo.get_all_tasks_of_project(project_id)
            
        if not tasks:
            raise TaskNotFound()
        
        return tasks