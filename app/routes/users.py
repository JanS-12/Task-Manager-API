from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.user_schema import UserSchema
from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.containers.user_container import DI

user_bp = Blueprint("users", __name__, url_prefix = "/api/v1/users")

@user_bp.route("", methods=["GET"])
@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["admin"]) 
def get_all_users():
    return DI.users_profile_controller.get(int(get_jwt_identity()))
 

@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_user(user_id: int):
    return DI.user_profile_controller.get(user_id, int(get_jwt_identity()))

    
@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_user(user_id: int):
    return DI.update_controller.update(user_id, int(get_jwt_identity()),  request.get_json())

 
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required(verify_type = False)
@role_required(["admin"])
def remove_user(user_id: int):   
    return DI.remove_controller.remove(user_id, int(get_jwt_identity()))