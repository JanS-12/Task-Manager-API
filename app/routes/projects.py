from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.project_schema import ProjectSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.containers.user_container import User_DI
from app.containers.project_container import Project_DI


project_bp = Blueprint("projects", __name__, url_prefix = "/api/v1/projects")

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many = True)

# GET /projects ---> List all projects
@project_bp.route("", methods=["GET"])
@project_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_projects():   
   return Project_DI.retrieve_projects_controller.get_projects(int(get_jwt_identity()))


# GET /projects/<int:project_id> ---> List a project
@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_project(project_id: int):
   return Project_DI.retrieve_project_controller.get_project(project_id, int(get_jwt_identity()))


# POST /projects/create ---> Create a Project
@project_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_project():
   return Project_DI.create_project_controller.create_project(request.get_json(), int(get_jwt_identity()))

# PUT /projects/<project_id> --> Update a project
@project_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_project(project_id: int):
    current_user_id = int(get_jwt_identity())
    data = request.get_json() 
    project = User_DI.project_service.update_project(data, project_id, current_user_id) 
    return project_schema.jsonify(project), 200
    
    
# DELETE /projects/<project_id> --> Delete a project and its tasks
@project_bp.route("/<int:project_id>", methods=["DELETE"])  
@jwt_required()
@role_required(["user", "admin"])
def remove_project(project_id: int):
    User_DI.project_service.remove_project(project_id, int(get_jwt_identity()))
    return jsonify(message = ""), 204