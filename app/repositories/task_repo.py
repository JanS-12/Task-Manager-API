from app.models.task import Task
from app.extensions import db

# Handles all CRUD for Tasks
class TaskRepository:
    def create_task(self, project_id, data):
        task = Task(
            title = data["title"],
            description = data.get("description"),
            project_id = project_id
        )
        
        db.session.add(task)
        db.session.commit()
        return task        
    
    def get_all_tasks(self):
        return Task.query.all()
    
    def get_all_tasks_of_project(self, project_id):
        return Task.query.filter_by(project_id = project_id).all()
    
    def get_a_task(self, task_id):
        return Task.query.filter_by(id = task_id).first()
    
    def update_task(self, task_id, data):
        task = Task.query.filter_by(id = task_id).first()
        
        if "title" in data: task.title = data["title"]
        if "description" in data: task.description = data.get("description")
        if "project_id" in data: task.project_id = data["project_id"]
        
        db.session.commit()
        return task
    
    def remove_task(self, task_id):
        task = Task.query.filter_by(id = task_id).first()
        db.session.delete(task)
        db.session.commit()
        