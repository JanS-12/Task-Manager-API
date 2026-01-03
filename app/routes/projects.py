from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.project_schema import ProjectSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.containers.user_container import DI


project_bp = Blueprint("projects", __name__, url_prefix = "/api/v1/projects")

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many = True)

# GET /projects ---> List all projects
@project_bp.route("", methods=["GET"])
@project_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_projects():   
    projects = DI.project_service.get_projects(int(get_jwt_identity()))
    return projects_schema.jsonify(projects), 200


# GET /projects/<int:project_id> ---> List a project
@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_project(project_id: int):
    project = DI.project_service.get_a_project(project_id, int(get_jwt_identity()))  
    return project_schema.jsonify(project), 200


# POST /projects/create ---> Create a Project
@project_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_project():
    project = DI.project_service.create_project(request.get_json(), int(get_jwt_identity()))
    return project_schema.jsonify(project), 201


# PUT /projects/<project_id> --> Update a project
@project_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_project(project_id: int):
    current_user_id = int(get_jwt_identity())
    data = request.get_json() 
    project = DI.project_service.update_project(data, project_id, current_user_id) 
    return project_schema.jsonify(project), 200
    
    
# DELETE /projects/<project_id> --> Delete a project and its tasks
@project_bp.route("/<int:project_id>", methods=["DELETE"])  
@jwt_required()
@role_required(["user", "admin"])
def remove_project(project_id: int):
  DI.project_service.remove_project(project_id, int(get_jwt_identity()))
  return jsonify(message = ""), 204