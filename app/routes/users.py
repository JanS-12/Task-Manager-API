from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema

# Input: username, email, password_hash

user_bp = Blueprint("users", __name__, url_prefix = "/users")

user_schema = UserSchema()
users_schema = UserSchema(many = True)

# GET /users/<user_id> --> Get all Users
@user_bp.route("", methods=["GET"])
def get_users():
    users = User.query.all()                # Get all users
    if users:
        return users_schema.jsonify(users), 200
    else:
        return jsonify(message = "User not found"), 404

# GET /users/<user_id> --> Get a Users
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = User.query.filter_by(user_id = user_id).first() # first() because should be one record
    if user:
        return user_schema.jsonify(user), 200
    else:
        return jsonify(message = "User not found"), 404

# POST /users/register
@user_bp.route("/register", methods=["POST"])
def create_user():
    data = request.get_json()
    if data:
        user = User(username=data["username"], email=data["email"], password_hash = data["password_hash"])
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user), 201
    else:
        return jsonify(message = "No data provided. Need data to proceed"), 400

# PUT /users/<user_id> --> Replace a user
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    user = User.query.filter_by(user_id = user_id).first()
    data = request.get_json()
    if user: 
        user.username = data["username"]
        user.email  = data["email"]
        user.password_hash = data["password_hash"]
        db.session.commit()                 # Commit changes to db
        return user_schema.jsonify(user), 200
    else:
        return jsonify(message = "User not found"), 404    
    
# DELETE /users/<user_id> --> Delete a user    
@user_bp.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id: int):   
    user = User.query.filter_by(user_id = user_id).first() 
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message = ""), 204   # Return nothing
    else:
        return jsonify(message = "User not found"), 404
    