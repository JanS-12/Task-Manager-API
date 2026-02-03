from app.services.projects.create_project import CreateProjectService
from app.schemas.project_schema import ProjectSchema
from app.utils.custom_exceptions import NoDataError

class CreateProjectController:
    def __init__(self, service: CreateProjectService):  
        self.service = service
        self.schema = ProjectSchema()
        
    def create_project(self, data, user_id):
        if not data or not user_id:
            raise NoDataError()
        
        project_data = self.schema.load(data)
        project = self.service.create_project(project_data, user_id)
        return self.schema.jsonify(project), 201