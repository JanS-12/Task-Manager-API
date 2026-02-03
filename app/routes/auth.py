from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.user_schema import UserSchema
from app.utils.security import  role_required
from flask import Blueprint, request, jsonify
from app.extensions import limiter
from app.containers.user_container import User_DI

auth_bp = Blueprint("auth", __name__, url_prefix = "/api/v1/auth")
user_schema = UserSchema()

# GET --> /api/v1/auth/health
@auth_bp.route("/health", methods=["GET"])
@limiter.limit("20 per minute") 
def health_check():
    return jsonify(message = "Auth reachable!")


# Register --> POST /api/v1/auth/register
@auth_bp.route("/register", methods=["POST"])
@limiter.limit("20 per minute")
def register():
    return User_DI.registration_controller.register(request.get_json())


# Login --> POST "/api/v1/auth/login"
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("100 per minute") 
def login():   
    tokens = User_DI.login_controller.login(request.get_json())
    return jsonify(access_token = tokens["access_token"], refresh_token = tokens["refresh_token"]), 200


# This function is to be called inUser_DIrectly by the front-end client, not the user User_DIrectly
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh_access_token():
    new_access_token = User_DI.auth_service.refresh_access_token(int(get_jwt_identity()))
    return jsonify(access_token = new_access_token), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def logout():
    User_DI.logout_controller.logout(int(get_jwt_identity()))
    return jsonify(message = "User succesfully logged out!"), 200