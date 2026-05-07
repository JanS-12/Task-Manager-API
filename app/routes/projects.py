from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, jsonify, current_app
from app.utils.security import role_required

project_bp = Blueprint("projects", __name__, url_prefix = "/api/v1/projects")


# GET /projects ---> List all projects
@project_bp.route("", methods=["GET"])
@project_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_projects():   
      project_container = current_app.container.project
      return project_container.retrieve_projects_controller.get_projects(int(get_jwt_identity()))


# GET /projects/<int:project_id> ---> List a project
@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_project(project_id: int):
      project_container = current_app.container.project
      return project_container.retrieve_project_controller.get_project(project_id, int(get_jwt_identity()))


# POST /projects/create ---> Create a Project
@project_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_project():
      project_container = current_app.container.project
      return project_container.create_controller.create_project(request.get_json(), int(get_jwt_identity()))

# PUT /projects/<project_id> --> Update a project
@project_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_project(project_id: int):
      current_user_id = int(get_jwt_identity())
      data = request.get_json() 
      project_container = current_app.container.project
      return project_container.update_controller.update_project(data, project_id, current_user_id) 
    
    
    
# DELETE /projects/<project_id> --> Delete a project and its tasks
@project_bp.route("/<int:project_id>", methods=["DELETE"])  
@jwt_required()
@role_required(["user", "admin"])
def remove_project(project_id: int):
      project_container = current_app.container.project
      project_container.remove_controller.remove_project(project_id, int(get_jwt_identity()))
      return jsonify(message = ""), 204