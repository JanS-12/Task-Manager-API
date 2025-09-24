from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.task import Task
from app.schemas.task_schema import TaskSchema

# Input: task_name, description, project_id

task_bp = Blueprint("tasks", __name__, url_prefix = "/projects/<int:project_id>/tasks")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)


# GET /projects/<project_id>/tasks --> get all tasks for a project
@task_bp.route("", methods=["GET"])
def get_tasks(project_id):
    tasks = Task.query.filter_by(project_id = project_id)
    if tasks:
        return tasks_schema.jsonify(tasks), 200
    else:
        return jsonify(message = "Task not found"), 404

# GET /projects/<project_id>/tasks/<task_id> --> get a task for a project
@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(project_id, task_id):
    task = Task.query.filter_by(project_id = project_id, task_id = task_id).first()
    if task:
        return task_schema.jsonify(task), 200
    else:
        return jsonify(message = "Task not found"), 404

# POST /projects/<project_id>/tasks/create  --> Create a task for a project
@task_bp.route("/create", methods=["POST"])
def create_task(project_id):
    data = request.get_json()
    if data:
        task = Task(task_name=data["task_name"], description=data.get("description"), project_id = project_id)
        db.session.add(task)
        db.session.commit()
        return task_schema.jsonify(task), 201
    else:
        return jsonify(message = "Invalid data"), 400

# PUT /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(project_id: int, task_id: int):
    task = Task.query.filter_by(project_id = project_id, task_id = task_id).first()
    data = request.get_json()
    if task:
        task.task_name = data["task_name"]
        task.description = data["description"]
        db.session.commit()
        return task_schema.jsonify(task), 200
    else:
        return jsonify(message = "Task not found"), 404
    
# DELETE /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["DELETE"])
def remove_task(project_id: int, task_id: int):
    task = Task.query.filter_by(project_id = project_id, task_id = task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify(message = ""), 204 
    else:
        return jsonify(message = "Task not found"), 404  