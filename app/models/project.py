from app.extensions import db
from sqlalchemy.sql import func

# Projects Table in DB
class Project(db.Model):
  __tablename__ = "projects"
  id            = db.Column(db.Integer, primary_key = True)
  title         = db.Column(db.String(80), nullable = False)
  description   = db.Column(db.Text)
  owner_id      = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False, index = True)
  created_at    = db.Column(db.DateTime(timezone = True), server_default = func.now())
  updated_at    = db.Column(db.DateTime(timezone = True), server_default = func.now(), onupdate = func.now())

  # Database Relationships
  owner         = db.relationship("User", back_populates = "projects")    # A project belongs to a user
  tasks         = db.relationship("Task", back_populates = "project" , cascade = "all, delete-orphan")     # A project can have on or multiple tasks