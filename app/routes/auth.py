from flask_jwt_extended import get_jwt_identity, jwt_required
from app.repositories.token_repo import TokenRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from app.utils.security import  role_required
from flask import Blueprint, request, jsonify
from app.utils.logging import get_logger
from app.extensions import limiter


auth_bp = Blueprint("auth", __name__, url_prefix = "/api/v1/auth")
user_schema = UserSchema()
auth_service = AuthService(TokenRepository(), UserService(UserRepository()))

# Loggers 
app_logger = get_logger("app")
auth_logger = get_logger("auth")
audit_logger = get_logger("audit")

# GET --> /api/v1/auth/health
@auth_bp.route("/health", methods=["GET"])
@limiter.limit("20 per minute") 
def health_check():
    return jsonify(message = "Auth reachable!")


# Register --> POST /api/v1/auth/register
@auth_bp.route("/register", methods=["POST"])
@limiter.limit("20 per minute")
def register():
    app_logger.info("Register endpoint reached.")
    new_user = auth_service.register_user(request.get_json())
    return user_schema.jsonify(new_user), 201


# Login --> POST "/api/v1/auth/login"
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("100 per minute") 
def login():   
    app_logger.info("Login endpoint reached.")
    tokens = auth_service.login(request.get_json())
    return jsonify(access_token = tokens["access_token"], refresh_token = tokens["refresh_token"]), 200


# This function is to be called indirectly by the front-end client, not the user directly
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh_access_token():
    new_access_token = auth_service.refresh_access_token(int(get_jwt_identity()))
    return jsonify(access_token = new_access_token), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def logout():
    auth_service.logout(int(get_jwt_identity()))
    return jsonify(message = "User succesfully logged out!"), 200