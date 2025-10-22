from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.task import Task
from app.models.project import Project
from app.schemas.task_schema import TaskSchema
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from app.utils.security import role_required

# Input: task_name, description, project_id

task_bp = Blueprint("tasks", __name__, url_prefix = "/api/v1/projects/<int:project_id>/tasks")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

# GET /projects/<project_id>/tasks --> get all tasks for a project
@task_bp.route("", methods=["GET"])
@task_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_tasks(project_id: int):
    project = Project.query.get_or_404(project_id)      # Get Project if exists
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
        
    if claims["role"] != "admin" and project.owner_id != current_user_id:    # Make sure proper ownership
        return jsonify(message = "Access Denied"), 403
    
    if claims["role"] == "admin": 
        tasks = Task.query.all()

    tasks = Task.query.filter_by(project_id = project_id).all()
    return tasks_schema.jsonify(tasks), 200


# GET /projects/<project_id>/tasks/<task_id> --> get a task for a project
@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_task(project_id: int, task_id: int):
    project = Project.query.get_or_404(project_id)      # Get Project if exists
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    if claims["role"] != "admin" and project.owner_id != current_user_id:
        return jsonify(message = "Access denied"), 403
    
    task = Task.query.get_or_404(task_id) # Check if specific tasks exists
    
    if task.project_id != project_id:
        return jsonify(message = "Access denied"), 403
    
    return task_schema.jsonify(task), 200
    

# POST /projects/<project_id>/tasks/create  --> Create a task for a project
@task_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_task(project_id: int):
    project = Project.query.get_or_404(project_id)      # Get Project if exists
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    json_data = request.get_json()
    
    # Check for input
    if not json_data:
        return jsonify(message = "Invalid data"), 400
    
    # Validate Input
    errors = task_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    
    # Check ownership
    if claims["role"] == "admin" or project.owner_id == current_user_id:
        # Deserialize data    
        data = task_schema.load(json_data)
            
        task = Task(
            task_name = data["task_name"], 
            description = data.get("description"), 
            project_id = project_id
        )
        db.session.add(task)
        db.session.commit()
        return task_schema.jsonify(task), 201
    
    return jsonify(message = "Access Denied"), 403


# PUT /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_task(project_id: int, task_id: int):
    project = Project.query.get_or_404(project_id)      # Get Project if exists
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    json_data = request.get_json()
    
    if claims["role"] != "admin" and project.owner_id != current_user_id:
        return jsonify(message = "Access Denied"), 403
    
    if not json_data:
        return jsonify(message = "No data provided."), 400   
    
    # Validate input
    errors = task_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    
    # Check if task exists
    task = Task.query.get_or_404(task_id) 
    
    # Deserialize data
    data = task_schema.load(json_data)
    
    task.task_name = data["task_name"]
    task.description = data["description"]
    db.session.commit()
    return task_schema.jsonify(task), 200
    
    
# DELETE /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
@role_required(["user", "admin"])
def remove_task(project_id: int, task_id: int):
    project = Project.query.get_or_404(project_id)      # Get Project if exists
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    if claims["role"] != "admin" and project.owner_id != current_user_id:
        return jsonify(message = "Access Denied"), 403
    
    task = Task.query.get_or_404(task_id)
    
    if task.project_id != project_id:
        return jsonify(message = "Access denied"), 403
    
    db.session.delete(task)
    db.session.commit()
    return jsonify(message = ""), 204 
      