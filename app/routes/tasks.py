from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.task_schema import TaskSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.di_container import DI

task_bp = Blueprint("tasks", __name__, url_prefix = "/api/v1/projects/<int:project_id>/tasks")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

# GET /projects/<project_id>/tasks --> get all tasks for a project
@task_bp.route("", methods=["GET"])
@task_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_tasks(project_id: int):
    tasks = DI.task_service.get_all_tasks(project_id, int(get_jwt_identity()))
    return tasks_schema.jsonify(tasks), 200


# GET /projects/<project_id>/tasks/<task_id> --> get a task for a project
@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_task(project_id: int, task_id: int):
    task = DI.task_service.get_a_task(project_id, task_id, int(get_jwt_identity()))
    return task_schema.jsonify(task), 200


# POST /projects/<project_id>/tasks/create  --> Create a task for a project
@task_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_task(project_id: int):
    data = request.get_json()
    current_user_id = int(get_jwt_identity())
    task = DI.task_service.create_task(data, project_id, current_user_id)
    return task_schema.jsonify(task), 201


# PUT /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_task(project_id: int, task_id: int):    
    current_user_id = int(get_jwt_identity())
    json_data = request.get_json()
    task = DI.task_service.update_task(json_data, project_id, task_id, current_user_id)
    return task_schema.jsonify(task), 200
    
    
# DELETE /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
@role_required(["user", "admin"])
def remove_task(project_id: int, task_id: int):
    current_user_id = int(get_jwt_identity())
    DI.task_service.remove_task(project_id, task_id, current_user_id)
    return jsonify(message = ""), 204 
      