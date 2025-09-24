from app.extensions import db
from sqlalchemy.sql import func

# Tasks Table in DB
class Task(db.Model):
    __tablename__ = "tasks"
    task_id          = db.Column(db.Integer, primary_key = True)
    task_name   = db.Column(db.String(80), nullable = False)
    description = db.Column(db.Text)
    project_id  = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable = False)
    created_at  = db.Column(db.DateTime(timezone = True), server_default = func.now())
    project     = db.relationship("Project", back_populates = "tasks")      # A Task belongs to a project