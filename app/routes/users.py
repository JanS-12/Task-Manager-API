from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.security import role_required
from flask import Blueprint, request, current_app

user_bp = Blueprint("users", __name__, url_prefix = "/api/v1/users")


@user_bp.route("", methods=["GET"])
@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["admin"]) 
def get_all_users():
    user_container = current_app.container.user
    return user_container.users_profile_controller.get(int(get_jwt_identity()))


@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_user(user_id: int):
    user_container = current_app.container.user
    return user_container.user_profile_controller.get(user_id, int(get_jwt_identity()))

    
@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required(["user", "admin"])
def update_user(user_id: int):
    user_container = current_app.container.user
    return user_container.update_controller.update(user_id, int(get_jwt_identity()),  request.get_json())

 
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required(verify_type = False)
@role_required(["admin"])
def remove_user(user_id: int):   
    user_container = current_app.container.user
    return user_container.remove_controller.remove(user_id, int(get_jwt_identity()))