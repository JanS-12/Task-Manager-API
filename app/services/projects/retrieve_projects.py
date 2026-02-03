from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.policies.project_policy import ProjectPolicy
from app.utils.custom_exceptions import UserNotFound, ProjectNotFound
    
class GetProjectsService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.policy = ProjectPolicy()
        
    def get_projects(self, requester_id):
        requester = self.user_repo.get_by_id(requester_id)
        if not requester:
            raise UserNotFound()
        
        if self.policy.can_view_all_projects(requester):
            projects = self.project_repo.get_all_projects()
        else:
            projects = self.project_repo.get_all_projects_of_user(requester.id)
    
        if not projects:
            raise ProjectNotFound()    
        
        return projects