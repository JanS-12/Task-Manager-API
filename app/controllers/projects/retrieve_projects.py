from app.services.projects.retrieve_projects import GetProjectsService
from app.schemas.project_schema import ProjectSchema
from app.utils.custom_exceptions import NoDataError

class GetProjectsController:
    def __init__(self, service: GetProjectsService):
        self.service = service
        self.schema = ProjectSchema(many = True)
    
    def get_projects(self, requester_id):
        if not requester_id:
            raise NoDataError()
        
        projects = self.service.get_projects(requester_id)
        return self.schema.jsonify(projects), 200