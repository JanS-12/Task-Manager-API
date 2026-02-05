from app.services.projects.update_project import UpdateProjectService
from app.schemas.project_schema import ProjectSchema
from app.utils.custom_exceptions import NoDataError

class UpdateProjectController:
    def __init__(self, service: UpdateProjectService):
        self.service = service
        self.schema = ProjectSchema()
        
    def update_project(self, data, project_id, user_id):
        if not data:
            raise NoDataError()
        
        project_data = self.schema.load(data)
        project = self.service.update_project(project_data, project_id, user_id)
        return self.schema.jsonify(project), 200