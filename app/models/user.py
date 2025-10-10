from app.extensions import db
from sqlalchemy.sql import func

# Users Table in DB
class User(db.Model):
  __tablename__ = "users"
  user_id       = db.Column(db.Integer, primary_key = True)
  username      = db.Column(db.String(80), unique = True, nullable = False)
  email         = db.Column(db.String(30), unique = True, nullable = False)
  role          = db.Column(db.String(10), nullable = False)
  password_hash = db.Column(db.String(128), nullable = False, default = "user")
  created_at    = db.Column(db.DateTime(timezone = True), server_default = func.now())
  updated_at    = db.Column(db.DateTime(timezone = True), server_default = func.now(), onupdate = func.now())
  
  # Database relationship
  projects      = db.relationship("Project", back_populates="owner")  # A user can have one or many projects