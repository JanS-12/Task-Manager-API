from app.utils.custom_exceptions import TaskNotFound, AccessDenied, NoDataError, TaskIncorrectProject
from app.services.project_service import ProjectService
from app.repositories.task_repo import TaskRepository
from app.services.user_service import UserService
from app.schemas.task_schema import TaskSchema
from app.utils.logging import get_logger

audit_logger = get_logger("audit")
class TaskService:
    def __init__(self, task_repo: TaskRepository, project_service: ProjectService, user_service: UserService):
        self.project_service = project_service
        self.user_service = user_service
        self.task_schema = TaskSchema()
        self.task_repo = task_repo
        
    def get_all_tasks(self, project_id, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        project = self.project_service.get_a_project(project_id, user.id)
        
        # Check privileges
        if user.role != "admin" and user.id != project.owner_id:
            raise AccessDenied()
        
        if user.role == "admin":        
            # Admin retrieves all tasks
            tasks = self.task_repo.get_all_tasks()
            audit_logger.info(f"Admin \"{user.username}\" retrieved all tasks.")
        else:
            # User gets task of their projects
            tasks = self.task_repo.get_all_tasks_of_project(project_id)
            audit_logger.info(f"User \"{user.username}\" retrieved all tasks from project \"{[project.title]}\".")
                    
        if not tasks:
            raise TaskNotFound()

        return tasks
    
    
    def get_a_task(self, project_id, task_id, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        project = self.project_service.get_a_project(project_id, user.id)
        
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        task = self.task_repo.get_a_task(task_id)
        if not task:
            raise TaskNotFound()
        
        if task.project_id != project.id:
            raise TaskIncorrectProject()
        
        audit_logger.info(f"User \"{user.username}\" retrieved task \"{task.title}\" with ID \'{task.id}\' from project \"{project.title}\".")
        return task
    
    
    def create_task(self, data, project_id, requester_id):
        if not data:
            raise NoDataError()
        
        user = self.user_service.get_user(requester_id, requester_id)
        project = self.project_service.get_a_project(project_id, user.id)
        
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        task_data = self.task_schema.load(data)
        task = self.task_repo.create_task(project_id, task_data)
        audit_logger.info(f"User \"{user.username}\" created task \"{task.title}\" with ID \'{task.id}\', under project \"{project.title}\".")
        return task
    
    
    def update_task(self, data, project_id, task_id, requester_id):
        if not data:
            raise NoDataError()
        
        user = self.user_service.get_user(requester_id, requester_id)
        project = self.project_service.get_a_project(project_id, user.id)
        task = self.task_repo.get_a_task(task_id)
        
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        if not task:
            raise TaskNotFound()

        if task.project_id != project.id:
            raise TaskIncorrectProject()
                
        task_data = self.task_schema.load(data)
        task = self.task_repo.update_task(task_id, task_data)
        
        audit_logger.info(f"User \"{user.username}\" has updated task with ID \'{task.id}\', \"{task.title}\".")
        return task
    
    
    def remove_task(self, project_id, task_id, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        project = self.project_service.get_a_project(project_id, user.id)
        task = self.task_repo.get_a_task(task_id)
        
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        if not task:
            raise TaskNotFound()
        
        if task.project_id != project.id:
            raise TaskIncorrectProject()
            
        self.task_repo.remove_task(task_id)
        audit_logger.info(f"User \"{user.username}\" has deleted task that had ID \'{task_id}\', under project \"{project.title}\".")
        
        
        
        
            