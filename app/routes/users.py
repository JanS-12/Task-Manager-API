from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.user_schema import UserSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.di_container import DI

# Input: username, email, password_hash
user_bp = Blueprint("users", __name__, url_prefix = "/api/v1/users")

# Schemas
user_schema = UserSchema()
users_schema = UserSchema(many = True)

# GET /users --> Get all Users
@user_bp.route("", methods=["GET"])
@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["admin"]) 
def get_all_users():
    users = DI.user_service.get_all_users(int(get_jwt_identity()))
    return users_schema.jsonify(users), 200
 
 # GET /user_id --> Get user profile
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_user(user_id: int):
    user = DI.user_service.get_user(user_id, int(get_jwt_identity()))
    return user_schema.jsonify(user), 200
    
# PUT /users/<user_id> --> Replace a user
@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_user(user_id: int):
    user = DI.user_service.update_user(user_id, request.get_json(), int(get_jwt_identity()))
    return user_schema.jsonify(user), 200

# DELETE /<user_id> --> Delete a user    
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required(verify_type = False)
@role_required(["admin"])
def remove_user(user_id: int):   
    DI.user_service.delete_user(user_id, int(get_jwt_identity()))
    return jsonify(""), 204