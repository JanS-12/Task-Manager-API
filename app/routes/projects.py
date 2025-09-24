from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.project import Project
from app.schemas.project_schema import ProjectSchema

# Input : project_name, description, owner_id

project_bp = Blueprint("projects", __name__, url_prefix = "/projects")

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


# GET /projects ---> List all projects
@project_bp.route("", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    
    if projects:
      return projects_schema.jsonify(projects), 200
    else:
      return jsonify(message = "Project not found"), 404

# GET /projects/<int:project_id> ---> List a project
@project_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id: int):
    project = Project.query.filter_by(project_id = project_id).first()
    
    if project:
      return project_schema.jsonify(project), 200
    else:
      return jsonify(message = "Project not found"), 404

# POST /projects/register ---> Create a Project
@project_bp.route("/register", methods=["POST"])
def create_project():
    data = request.get_json()
    if data:
      project = Project(project_name=data["project_name"], description=data.get("description"), owner_id = data["owner_id"])
      db.session.add(project)
      db.session.commit()
      return project_schema.jsonify(project), 201
    else:
      return jsonify(message = "No data provided, need data to proceed"), 400

# PUT /projects/<project_id> --> Update a project
@project_bp.route("/<int:project_id>", methods=["PUT"])
def update_project(project_id: int):
    project = Project.query.filter_by(project_id = project_id).first()
    data = request.get_json() 
    if project and data:
      project.project_name = data["project_name"]
      project.description = data["description"]      
      db.session.commit()
      return project_schema.jsonify(project), 200
    else:
      return jsonify(message = "Invalid input"), 400
    
# DELETE /projects/<project_id> --> Delete a project and its tasks
@project_bp.route("/<int:project_id>", methods=["DELETE"])  
def remove_project(project_id: int):
  project = Project.query.filter_by(project_id = project_id).first()
  if project:
    db.session.delete(project)
    db.session.commit()
    return jsonify(message = ""), 204
  else:
    return jsonify(message = "Project not found"), 404