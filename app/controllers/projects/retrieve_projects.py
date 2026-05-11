from app.services.projects.retrieve_projects import GetProjectsService
from app.utils.responses import build_success_response
from app.schemas.project_schema import ProjectSchema
from app.utils.custom_exceptions import NoDataError
from flask import jsonify
class GetProjectsController:
    def __init__(self, service: GetProjectsService):
        self.service = service
        self.schema = ProjectSchema(many = True)
    
    def get_projects(self, requester_id):
        if not requester_id:
            raise NoDataError()
        
        projects = self.service.get_projects(requester_id)
        return jsonify(
            build_success_response(
                "Projects retrieved successfully",
                200, 
                self.schema.dump(projects)
            )
        ), 200