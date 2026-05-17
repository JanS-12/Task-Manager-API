from app.schemas.projects.project_response_schema import ProjectResponseSchema
from app.schemas.projects.update_project_schema import UpdateProjectSchema
from app.services.projects.update_project import UpdateProjectService
from app.utils.responses import build_success_response
from flask import jsonify
class UpdateProjectController:
    def __init__(self, service: UpdateProjectService):
        self.service = service
        self.update_schema = UpdateProjectSchema()
        self.response_schema = ProjectResponseSchema()
        
    def update_project(self, data, project_id, user_id):
        validated = self.update_schema.load(data, partial = True)
        project = self.service.update_project(validated, project_id, user_id)
        return jsonify(
            build_success_response(
                "Project updated successfully",
                200,
                self.response_schema.dump(project)
            )
        ), 200