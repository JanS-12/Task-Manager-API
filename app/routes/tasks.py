from app.utils.custom_exceptions import AccessDenied, ProjectNotFound, TaskNotFound, TaskIncorrectProject, NoDataError
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from app.schemas.task_schema import TaskSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.models.project import Project
from app.models.task import Task
from app.extensions import db

task_bp = Blueprint("tasks", __name__, url_prefix = "/api/v1/projects/<int:project_id>/tasks")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

# GET /projects/<project_id>/tasks --> get all tasks for a project
@task_bp.route("", methods=["GET"])
@task_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_tasks(project_id: int):
    project = Project.query.filter_by(id = project_id).first()      # Get Project if exists
    if not project:
        raise ProjectNotFound()
      
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
        
    if claims["role"] != "admin" and project.owner_id != current_user_id:    # Make sure proper ownership
        raise AccessDenied()  
    
    tasks = Task.query.filter_by(project_id = project_id).all()
    
    if claims["role"] == "admin": 
        tasks = Task.query.all()
        
    if not tasks:
        return jsonify(message = "No tasks for this project this time."), 404
    
    return tasks_schema.jsonify(tasks), 200


# GET /projects/<project_id>/tasks/<task_id> --> get a task for a project
@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_task(project_id: int, task_id: int):
    project = Project.query.filter_by(id = project_id).first()      # Get Project if exists
    if not project:
        raise ProjectNotFound()
    
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    if claims["role"] != "admin" and project.owner_id != current_user_id:
        raise AccessDenied()
    
    task = Task.query.filter_by(id = task_id).first() # Check if specific tasks exists
    if not task:
        raise TaskNotFound()
    
    if task.project_id != project_id:
        raise TaskIncorrectProject()
    
    return task_schema.jsonify(task), 200
    

# POST /projects/<project_id>/tasks/create  --> Create a task for a project
@task_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_task(project_id: int):
    project = Project.query.filter_by(id = project_id).first()      # Get Project if exists
    if not project:
        raise ProjectNotFound()
    
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    json_data = request.get_json()
    
    # Check for input
    if not json_data:
        raise NoDataError()
    
    # Check ownership
    if claims["role"] == "admin" or project.owner_id == current_user_id:
        # Validate and deserialize data    
        data = task_schema.load(json_data)
            
        task = Task(
            title = data["title"], 
            description = data.get("description"), 
            project_id = project_id
        )
        db.session.add(task)
        db.session.commit()
        return task_schema.jsonify(task), 201
    
    raise AccessDenied()


# PUT /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_task(project_id: int, task_id: int):
    project = Project.query.filter_by(id = project_id).first()      # Get Project if exists
    if not project:
        raise ProjectNotFound()
    
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    json_data = request.get_json()
    
    if claims["role"] != "admin" and project.owner_id != current_user_id:
        raise AccessDenied()
    
    if not json_data:
        raise NoDataError()
    
    # Check if task exists
    task = Task.query.filter_by(id = task_id).first()
    if not task:    
        raise TaskNotFound() 
    
    # Validate and deserialize data
    data = task_schema.load(json_data)
    
    task.title = data["title"]
    task.description = data["description"]
    db.session.commit()
    return task_schema.jsonify(task), 200
    
    
# DELETE /projects/<project_id>/tasks/<task_id>
@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
@role_required(["user", "admin"])
def remove_task(project_id: int, task_id: int):
    project = Project.query.filter_by(id = project_id).first()      # Get Project if exists
    if not project:
        raise ProjectNotFound()
    
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    if claims["role"] != "admin" and project.owner_id != current_user_id:
        raise AccessDenied()
    
    task = Task.query.filter_by(id = task_id).first()
    if not task:    
        raise TaskNotFound() 
    
    if task.project_id != project_id:
        raise TaskIncorrectProject()
    
    db.session.delete(task)
    db.session.commit()
    return jsonify(message = ""), 204 
      