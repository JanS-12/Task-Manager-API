from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.project import Project
from app.schemas.project_schema import ProjectSchema
from app.utils.security import role_required
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.utils.custom_exceptions import BadRequest, Forbidden, ResourceNotFound, UnprocessableEntity

# Input : project_name, description, owner_id

project_bp = Blueprint("projects", __name__, url_prefix = "/api/v1/projects")

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many = True)


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
    else:
        projects = Project.query.filter_by(owner_id = current_user_id).all()
        
    if projects:  
      return projects_schema.jsonify(projects), 200    
  
    raise ResourceNotFound("No projects found")


# GET /projects/<int:project_id> ---> List a project
@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_project(project_id: int):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    project = Project.query.filter_by(id = project_id).first()
    if not project:
      raise ResourceNotFound("Project not found")
    
    if claims["role"] == "admin" or project.owner_id == current_user_id:
        return project_schema.jsonify(project), 200
    
    raise Forbidden("Access Denied")  


# POST /projects/register ---> Create a Project
@project_bp.route("/register", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def create_project():
    current_user_id = int(get_jwt_identity())
    json_data = request.get_json()
    if not json_data:               # Check for valid input
      raise BadRequest("No input data provided")  
    
    errors = project_schema.validate(json_data)   # Validate input
    if errors:
      raise UnprocessableEntity(errors)
    
    # Deserialize data
    data = project_schema.load(json_data)
    
    project = Project(title=data["title"], description=data.get("description"), owner_id = current_user_id)
    db.session.add(project)
    db.session.commit()
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
      raise BadRequest("No input data provided")  
    
    # Validate input
    errors = project_schema.validate(json_data)
    if errors:
      raise UnprocessableEntity(errors)
    
    # Check if project exists
    project = Project.query.filter_by(id = project_id).first()  
    if not project:
      raise ResourceNotFound("Project not found")
    
    if claims["role"] == "admin" or project.owner_id == current_user_id:
      # Deserialize data
      data = project_schema.load(json_data)
      
      project.title = data["title"]
      project.description = data["description"]      
      db.session.commit()
      return project_schema.jsonify(project), 200
    
    raise Forbidden("Access Denied")  
    
    
# DELETE /projects/<project_id> --> Delete a project and its tasks
@project_bp.route("/<int:project_id>", methods=["DELETE"])  
@jwt_required()
@role_required(["user", "admin"])
def remove_project(project_id: int):
  current_user_id = int(get_jwt_identity())
  claims = get_jwt()
  project = Project.query.filter_by(id = project_id).first()
  if not project:
    raise ResourceNotFound("Project not found")
  
  if claims["role"] == "admin" or project.owner_id == current_user_id:
    db.session.delete(project)
    db.session.commit()
    return jsonify(message = ""), 204
  
  raise Forbidden("Access Denied")