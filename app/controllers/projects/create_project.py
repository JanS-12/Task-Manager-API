from app.schemas.projects.project_response_schema import ProjectResponseSchema
from app.schemas.projects.create_project_schema import CreateProjectSchema
from app.services.projects.create_project import CreateProjectService
from app.utils.responses import build_success_response
from flask import jsonify
class CreateProjectController:
    def __init__(self, service: CreateProjectService):  
        self.service = service
        self.response_schema = ProjectResponseSchema()
        self.create_schema = CreateProjectSchema()
        
    def create_project(self, data, user_id):
        validated = self.create_schema.load(data)
        project = self.service.create_project(validated, user_id)
        return jsonify(
            build_success_response(
                "Project created successfully",
                201, 
                self.response_schema.dump(project)
            )
        ), 201