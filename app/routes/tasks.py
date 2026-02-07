from flask_jwt_extended import get_jwt_identity, jwt_required
from app.containers.task_container import Task_DI
from flask import Blueprint, request, jsonify
from app.utils.security import role_required

task_bp = Blueprint("tasks", __name__, url_prefix = "/api/v1/projects/<int:project_id>/tasks")

# GET /projects/<project_id>/tasks --> get all tasks for a project
@task_bp.route("", methods=["GET"])
@task_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_tasks(project_id: int):
    return Task_DI.retrieve_tasks_controller.get_tasks(project_id, int(get_jwt_identity()))


# GET /projects/<project_id>/tasks/<task_id> --> get a task for a project
@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_task(project_id: int, task_id: int):
    return Task_DI.retrieve_task_controller.get_task(project_id, task_id, int(get_jwt_identity()))
    

# POST /projects/<project_id>/tasks/create  --> Create a task for a project
@task_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_task(project_id: int):
    data = request.get_json()
    current_user_id = int(get_jwt_identity())
    return Task_DI.create_task_controller.create_task(data, project_id, current_user_id)
     

# PUT /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_task(project_id: int, task_id: int):    
    current_user_id = int(get_jwt_identity())
    json_data = request.get_json()
    return Task_DI.update_task_controller.update_task(json_data, project_id, task_id, current_user_id)
    
    
# DELETE /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
@role_required(["user", "admin"])
def remove_task(project_id: int, task_id: int):
    current_user_id = int(get_jwt_identity())
    Task_DI.remove_task_controller.remove_task(project_id, task_id, current_user_id)
    return jsonify(message = ""), 204 
      