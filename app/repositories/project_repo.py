from app.models.project import Project
from app.extensions import db

# Handles all CRUD for Projects
class ProjectRepository:
    def create_project(self, owner_id, data):
        print("Creating project, repo")
        project = Project(
            title = data["title"],
            description = data.get("description"),
            owner_id = owner_id
        )
        
        db.session.add(project)
        db.session.commit()
        return project
        
        
    def get_all_projects(self):
        return Project.query.all()
    
    
    def get_all_projects_of_user(self, user_id):
        return Project.query.filter_by(owner_id = user_id).all()
    
    
    def get_a_project(self, project_id):
        return Project.query.filter_by(id = project_id).first()
    
    
    def update_project(self, project_id, data):
        project = Project.query.filter_by(id = project_id).first()
        
        if "title" in data: project.title = data["title"]
        if "description" in data: project.description = data.get("description")
        if "owner_id" in data: project.owner_id = data["owner_id"]
        
        db.session.commit()
        return project
    
    def delete_project(self, project_id):
        project = Project.query.get(project_id)
        db.session.delete(project)
        db.session.commit()

    
   
        