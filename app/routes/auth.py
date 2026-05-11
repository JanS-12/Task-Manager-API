from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.security import  role_required
from flask import Blueprint, request, jsonify, current_app
from app.extensions import limiter

auth_bp = Blueprint("auth", __name__, url_prefix = "/api/v1/auth")

# GET --> /api/v1/auth/health
@auth_bp.route("/health", methods=["GET"])
@limiter.limit("20 per minute") 
def health_check():
    return jsonify(message = "Auth reachable!")


# Register --> POST /api/v1/auth/register
@auth_bp.route("/register", methods=["POST"])
@limiter.limit("20 per minute")
def register():
    user_container = current_app.container.user
    return user_container.registration_controller.register(request.get_json())


# Login --> POST "/api/v1/auth/login"
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("100 per minute") 
def login():   
    user_container = current_app.container.user
    return user_container.login_controller.login(request.get_json())


# This function is to be called inUser_DIrectly by the front-end client, not the user user_containerrectly
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh_access_token():
    user_container = current_app.container.user
    return user_container.refresh_access_token_controller.refresh_access_token(int(get_jwt_identity()))    


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def logout():
    user_container = current_app.container.user
    return user_container.logout_controller.logout(int(get_jwt_identity()))
    