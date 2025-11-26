from app.models.user import User
from app.extensions import db
from flask import jsonify
from app.utils.security import hash_password

# Handles all database CRUD functionalities
class UserRepository:
    def create(self, data):
        user = User(
            username = data["username"],
            password = hash_password(data["password"]),
            email = data["email"],
            role = data["role"]
        )
        db.session.add(user)
        db.session.commit()
        return user

    def get_by_id(self, id):
        return User.query.get(id)
    
    def get_by_username(self, username):
        return User.query.filter_by(username = username).first()
    
    def get_by_email(self, email):
        return User.query.filter_by(email = email).first()
    
    def get_all_users(self):
        return User.query.all()
    
    def update(self, id, data):
        user = User.query.get(id)
        
        if "username" in data: user.username = data["username"]
        if "email" in data: user.email = data["email"]
        if "password" in data: user.password = hash_password(data["password"])
        if "role" in data: user.role = data["role"]
        
        db.session.commit()
        return user
        
    def delete(self, id):
        try:
            user = User.query.get(id)
            db.session.delete(user)
            return jsonify({"message": "User deleted successfully"})
        except ExceptionGroup as e:
            # Failure --> Transaction Aborted, rollback automatically, but just to be sure we call it
            db.session.rollback()
            return jsonify(message = f"Error deleting user: {str(e)}"), 500
        # Don't return anything for now