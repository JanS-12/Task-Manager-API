from app.services.projects.remove_project import RemoveProjectService
from app.utils.custom_exceptions import NoDataError

class RemoveProjectController:
    def __init__(self, service: RemoveProjectService):
        self.service = service
        
    def remove_project(self, project_id, user_id): 
        if not user_id or not project_id:
            raise NoDataError()
        
        self.service.remove_project(project_id, user_id)