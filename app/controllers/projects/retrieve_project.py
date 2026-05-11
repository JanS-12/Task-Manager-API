from app.services.projects.retrieve_project import GetProjectService
from app.utils.responses import build_success_response
from app.schemas.project_schema import ProjectSchema
from app.utils.custom_exceptions import NoDataError
from flask import jsonify

class GetProjectController:
    def __init__(self, service: GetProjectService):
        self.service = service
        self.schema = ProjectSchema()
        
    def get_project(self, project_id, requester_id):
        if not project_id or not requester_id:
            raise NoDataError()
        
        project = self.service.get_project(project_id, requester_id)
        return jsonify(
            build_success_response(
                "Project retrieved successfully",
                200, 
                self.schema.dump(project)
            )
        ), 200