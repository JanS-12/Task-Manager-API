from app.utils.custom_exceptions import ProjectNotFound, AccessDenied, NoDataError
from app.repositories.project_repo import ProjectRepository
from app.schemas.project_schema import ProjectSchema
from app.services.user_service import UserService
from app.utils.logging import get_logger

audit_logger = get_logger("audit")
    
class ProjectService():
    def __init__(self, user_service: UserService, project_repo: ProjectRepository):
        self.user_service = user_service
        self.project_repo = project_repo
        self.project_schema = ProjectSchema()
        
    def get_projects(self, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        
        # If admin, retrieve all project, else only projects for user
        if user.role == "admin":
            projects = self.project_repo.get_all_projects()
            audit_logger.info(f"Admin \"{user.username}\" retrieved all projects.")
        else:
            projects = self.project_repo.get_all_projects_of_user(user.id)
            audit_logger.info(f"User \"{user.username}\" retrieved all of their projects.")
            
        if not projects:
            raise ProjectNotFound()
            
        return projects
    
    def get_a_project(self, project_id, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        
        project = self.project_repo.get_a_project(project_id)
        if not project:
            raise ProjectNotFound()
        
        if user.role != "admin" and user.id != project.owner_id:
            raise AccessDenied()
        
        audit_logger.info(f"User \"{user.username}\" retrieved project \"{project.title}\" with project ID \'{project.id}\'.")
        return project
        
        
    def create_project(self, data, requester_id):
        if not data:
            raise NoDataError()
        
        user = self.user_service.get_user(requester_id, requester_id)
        project_data = self.project_schema.load(data)
        project = self.project_repo.create_project(requester_id, project_data)
        
        audit_logger.info(f"User \"{user.username}\" has created project \"{project.title}\" with ID \'{project.id}\'.")
        return project
    
    def update_project(self, data, project_id, requester_id):
        if not data: 
            raise NoDataError()
        
        user = self.user_service.get_user(requester_id, requester_id)
        project = self.project_repo.get_a_project(project_id)
        project_data = self.project_schema.load(data)
        
        if not project:
            raise ProjectNotFound()
        
        if user.id != project.owner_id and user.role != "admin":
            raise AccessDenied()
        
        project = self.project_repo.update_project(project_id, project_data)
        audit_logger.info(f"User \"{user.username}\" has updated project with ID \'{project.id}\', \"{project.title}\".")
        return project
    
    def remove_project(self, project_id, requester_id):
        project = self.project_repo.get_a_project(project_id)
        user = self.user_service.get_user(requester_id, requester_id)
        if not project:
            raise ProjectNotFound()
        
        if user.role != "admin" and user.id != project.owner_id:
            raise AccessDenied()
    
        self.project_repo.delete_project(project_id)
        audit_logger.info(f"User \"{user.username}\" has deleted project that had ID \'{project_id}\'.")    
        
        
        
        
        
        
        
        
        
        
        
    
    
        