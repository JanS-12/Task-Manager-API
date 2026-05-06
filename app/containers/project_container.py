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

class ProjectContainer:
    def __init__(
        self, 
        user_repository=None,
        project_repository=None,
        task_repository=None
    ):
        
        # Dependencies (can be overridden in tests)
        self.project_repository = project_repository or ProjectRepository()
        self.user_repository = user_repository or UserRepository()
        self.task_repository = task_repository or TaskRepository()
        
        # Services 
        self.retrieve_project_service = GetProjectService(self.project_repository, self.user_repository) 
        self.retrieve_projects_service = GetProjectsService(self.project_repository, self.user_repository)
        self.create_project_service = CreateProjectService(self.project_repository, self.user_repository)
        self.update_project_service = UpdateProjectService(self.project_repository, self.user_repository)
        self.remove_project_service = RemoveProjectService(self.project_repository, self.user_repository)
        
        # Controllers
        self.retrieve_projects_controller = GetProjectsController(self.retrieve_projects_service) 
        self.remove_project_controller = RemoveProjectController(self.remove_project_service)
        self.retrieve_project_controller = GetProjectController(self.retrieve_project_service)
        self.update_project_controller = UpdateProjectController(self.update_project_service)
        self.create_project_controller = CreateProjectController(self.create_project_service)