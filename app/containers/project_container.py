from app.services.projects.retrieve_projects import GetProjectsService
from app.services.projects.create_project import CreateProjectService
from app.services.projects.update_project import UpdateProjectService
from app.services.projects.remove_project import RemoveProjectService
from app.services.projects.retrieve_project import GetProjectService

from app.controllers.projects.retrieve_projects import GetProjectsController
from app.controllers.projects.create_project import CreateProjectController
from app.controllers.projects.update_project import UpdateProjectController
from app.controllers.projects.remove_project import RemoveProjectController
from app.controllers.projects.retrieve_project import GetProjectController

from app.repositories.project_repo import ProjectRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.user_repo import UserRepository

class Project_DI:
    project_repository = None
    user_repository = None
    task_repository = None
    
    retrieve_project_service = None
    retrieve_project_controller = None
    
    retrieve_projects_service = None
    retrieve_projects_controller = None
    
    create_project_service = None
    create_project_controller = None
    
    update_project_service = None
    update_project_controller = None
    
    remove_project_service = None
    remove_project_controller = None
    
    def register_project_dependencies():
        Project_DI.user_repository = UserRepository()
        Project_DI.project_repository = ProjectRepository()
        Project_DI.task_repository = TaskRepository()
        
        Project_DI.retrieve_project_service = GetProjectService(Project_DI.project_repository, Project_DI.user_repository)
        Project_DI.retrieve_project_controller = GetProjectController(Project_DI.retrieve_project_service)
        
        Project_DI.retrieve_projects_service = GetProjectsService(Project_DI.project_repository, Project_DI.user_repository)
        Project_DI.retrieve_projects_controller = GetProjectsController(Project_DI.retrieve_projects_service)
    
        Project_DI.create_project_service = CreateProjectService(Project_DI.project_repository, Project_DI.user_repository)
        Project_DI.create_project_controller = CreateProjectController(Project_DI.create_project_service)
        
        Project_DI.update_project_service = UpdateProjectService(Project_DI.project_repository, Project_DI.user_repository)
        Project_DI.update_project_controller = UpdateProjectController(Project_DI.update_project_service)
        
        Project_DI.remove_project_service = RemoveProjectService(Project_DI.project_repository, Project_DI.user_repository)
        Project_DI.remove_project_controller = RemoveProjectController(Project_DI.remove_project_service)