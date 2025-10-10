from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.utils.security import hash_password, role_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
# Status codes are critical:

# 200 OK → success
# 201 Created → new resource made
# 204 No Content → deletion success
# 400 Bad Request → invalid input
# 401 Unauthorized → missing/invalid auth
# 403 Forbidden
# 404 Not Found → resource doesn’t exist
# 409 Conflict 
# 500 Internal Server Error → server issue

# Input: username, email, password_hash
user_bp = Blueprint("users", __name__, url_prefix = "/api/v1/users")

user_schema = UserSchema()
users_schema = UserSchema(many = True)

# GET /users --> Get all Users
@user_bp.route("", methods=["GET"])
@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["admin"]) 
def get_all_users():
    users = User.query.all()     
    if users:# Get all users
        return users_schema.jsonify(users), 200

    return jsonify(message = "No users found."), 404
 
 # GET /user_id --> Get user profile
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_user(user_id: int):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    # Check ownership
    if claims["role"] == "admin" or user_id == current_user_id: 
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user), 200
    
    return jsonify(error = "Access Denied"), 403
    
    

# PUT /users/<user_id> --> Replace a user
@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_user(user_id: int):
    # Check for input
    json_data = request.get_json()
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    if not json_data:
        return jsonify(message = "No data provided."), 400
    
    # Validate input 
    errors = user_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    
    if claims["role"] == "admin" or user_id == current_user_id:    
        # Check if user exists
        user = User.query.get_or_404(user_id)
        
        # Deserialize data
        data = user_schema.load(json_data)
        
        user.username = data["username"]
        user.email = data["email"]
        user.password_hash = hash_password(data["password_hash"])
        user.role  = data["role"]
        db.session.commit()                 # Commit changes to db
        return user_schema.jsonify(user), 200
    
    return jsonify(message = "Access Denied"), 403


# DELETE /<user_id> --> Delete a user    
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def remove_user(user_id: int):   
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message = ""), 204   # Return nothing
    