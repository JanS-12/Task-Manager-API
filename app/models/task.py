from app.extensions import db
from sqlalchemy.sql import func

# Tasks Table in DB
class Task(db.Model):
    __tablename__   = "tasks"
    id              = db.Column(db.Integer, primary_key = True)
    title           = db.Column(db.String(80), nullable = False)
    description     = db.Column(db.Text)
    project_id      = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable = False, index = True)
    created_at      = db.Column(db.DateTime(timezone = True), server_default = func.now())
    updated_at      = db.Column(db.DateTime(timezone = True), server_default = func.now(), onupdate = func.now())
    
    # Database Relationship
    project         = db.relationship("Project", back_populates = "tasks")      # A Task belongs to a project