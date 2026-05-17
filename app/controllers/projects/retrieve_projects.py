from app.schemas.projects.project_response_schema import ProjectResponseSchema
from app.services.projects.retrieve_projects import GetProjectsService
from app.utils.responses import build_success_response
from flask import jsonify
class GetProjectsController:
    def __init__(self, service: GetProjectsService):
        self.service = service
        self.response_schema = ProjectResponseSchema(many = True)
    
    def get_projects(self, requester_id):
        projects = self.service.get_projects(requester_id)
        return jsonify(
            build_success_response(
                "Projects retrieved successfully",
                200, 
                self.response_schema.dump(projects)
            )
        ), 200