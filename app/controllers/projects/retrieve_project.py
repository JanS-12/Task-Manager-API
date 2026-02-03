from app.services.projects.retrieve_project import GetProjectService
from app.schemas.project_schema import ProjectSchema
from app.utils.custom_exceptions import NoDataError

class GetProjectController:
    def __init__(self, service: GetProjectService):
        self.service = service
        self.schema = ProjectSchema()
        
    def get_project(self, project_id, requester_id):
        if not project_id or not requester_id:
            raise NoDataError()
        
        project = self.service.get_project(project_id, requester_id)
        return self.schema.jsonify(project), 200