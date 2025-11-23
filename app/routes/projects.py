from app.utils.custom_exceptions import NoDataError, AccessDenied, ProjectNotFound
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.schemas.project_schema import ProjectSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.utils.logging import get_logger
from app.models.project import Project
from app.extensions import db

project_bp = Blueprint("projects", __name__, url_prefix = "/api/v1/projects")

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many = True)

app_logger = get_logger("app")
audit_logger = get_logger("audit")

# GET /projects ---> List all projects
@project_bp.route("", methods=["GET"])
@project_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_projects():   
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
   
    if claims["role"] == "admin":
        projects = Project.query.all()
        audit_logger.info(f"Admin with ID \'{claims["sub"]}\' accessed all projects.")    
    else:
        projects = Project.query.filter_by(owner_id = current_user_id).all()
        audit_logger.info(f"User with ID \'{current_user_id}\' accessed their projects.")
        
    if projects:  
      return projects_schema.jsonify(projects), 200    
  
    raise ProjectNotFound()


# GET /projects/<int:project_id> ---> List a project
@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_project(project_id: int):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    app_logger.info(f"User with ID \'{current_user_id}\' wants to retrieve a project.")
    
    project = Project.query.filter_by(id = project_id).first()
    if not project:
      raise ProjectNotFound()
    
    if claims["role"] == "admin" or project.owner_id == current_user_id:
      audit_logger.info(f"User with ID \'{current_user_id}\' retrieved project \"{project.title}\" with ID \'{project.id}\'.")
      return project_schema.jsonify(project), 200
    
    raise AccessDenied()  


# POST /projects/create ---> Create a Project
@project_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_project():
    current_user_id = int(get_jwt_identity())
    json_data = request.get_json()
    
    app_logger.info(f"User ID \'{current_user_id}\' is trying to create a project.")
    if not json_data:               # Check for valid input
      raise NoDataError()  
    
    # Validate and deserialize data
    data = project_schema.load(json_data)
    
    project = Project(title=data["title"], description=data.get("description"), owner_id = current_user_id)
    db.session.add(project)
    db.session.commit()
    audit_logger.info(f"User ID \'{current_user_id}\' has successfully created project \"{project.title}\" with ID \'{project.id}\'.")
    return project_schema.jsonify(project), 201


# PUT /projects/<project_id> --> Update a project
@project_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_project(project_id: int):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    json_data = request.get_json() 
    # Check for valid input
    if not json_data:
      raise NoDataError()  
    
    # Check if project exists
    project = Project.query.filter_by(id = project_id).first()  
    if not project:
      raise ProjectNotFound()
    
    app_logger.info(f"User ID \'{current_user_id}\' is trying to update project \"{project.title}\" with ID \'{project.id}\'.")
    
    if claims["role"] == "admin" or project.owner_id == current_user_id:
      # Validate and deserialize data
      data = project_schema.load(json_data)
      
      project.title = data["title"]
      project.description = data["description"]      
      db.session.commit()
      audit_logger.info(f"User ID \'{current_user_id}\' has updated project with ID \'{project.id}\' successfully.")
      return project_schema.jsonify(project), 200
    
    raise AccessDenied()  
    
    
# DELETE /projects/<project_id> --> Delete a project and its tasks
@project_bp.route("/<int:project_id>", methods=["DELETE"])  
@jwt_required()
@role_required(["user", "admin"])
def remove_project(project_id: int):
  current_user_id = int(get_jwt_identity())
  claims = get_jwt()
  project = Project.query.filter_by(id = project_id).first()
  if not project:
    raise ProjectNotFound()
  
  app_logger.info(f"User ID \'{current_user_id}\' is trying to delete project \"{project.title}\" with ID \'{project.id}\'.")
  
  if claims["role"] == "admin" or project.owner_id == current_user_id:
    db.session.delete(project)
    db.session.commit()
    audit_logger.info(f"User ID \'{current_user_id}\' succesfully deleted project ID \'{project_id}\'.")
    return jsonify(message = ""), 204
  
  raise AccessDenied()