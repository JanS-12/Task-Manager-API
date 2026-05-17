from app.schemas.projects.project_response_schema import ProjectResponseSchema
from app.services.projects.retrieve_project import GetProjectService
from app.utils.responses import build_success_response
from flask import jsonify

class GetProjectController:
    def __init__(self, service: GetProjectService):
        self.service = service
        self.response_schema = ProjectResponseSchema()
        
    def get_project(self, project_id, requester_id):
        project = self.service.get_project(project_id, requester_id)
        return jsonify(
            build_success_response(
                "Project retrieved successfully",
                200, 
                self.response_schema.dump(project)
            )
        ), 200