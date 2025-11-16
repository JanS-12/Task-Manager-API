from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity)
from app.utils.custom_exceptions import NoDataError, InvalidCredentialsError, ExistingCredentialsError
from app.utils.security import hash_password, check_password
from app.utils.jwt import create_token_blocklist
from flask import Blueprint, request, jsonify
from app.schemas.user_schema import UserSchema
from app.extensions import db, limiter
from app.models.user import User

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
    json_data = request.get_json()
    # Check for input
    if not json_data:
        raise NoDataError()
 
    # Validate and deserialize data
    data = user_schema.load(json_data)
    
    # If user exists
    if User.query.filter_by(username = data["username"], email = data["email"]).first():
        raise ExistingCredentialsError()
    
    new_user = User(
        username = data["username"], 
        email = data["email"], 
        password = hash_password(data["password"]), # .decode("utf-8") --> to convert from bytes to str for DB
        role = data["role"]
    ) 
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201


# Login --> POST "/api/v1/auth/login"
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("100 per minute") 
def login():
    json_data = request.get_json()
    if not json_data:
        raise NoDataError()
    
    username = json_data.get("username")
    password = json_data.get("password")
    
    user = User.query.filter_by(username = username).first()    
    
    if not user or not check_password(password, user.password):
        raise InvalidCredentialsError()
    
    # Create both Access and Refresh Tokens
    additional_claims = {"role": user.role}
    access_token = create_access_token(
        identity = str(user.id), 
        additional_claims = additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity = str(user.id), 
        additional_claims = additional_claims
    )
    
    # Record JTI's for revocation
    tokens_blocklist = [
        create_token_blocklist(access_token),
        create_token_blocklist(refresh_token)
    ]
    
    db.session.add_all(tokens_blocklist)
    db.session.commit()   
    
    return jsonify(access_token = access_token, refresh_token = refresh_token), 200


# This function is to be called indirectly by the front-end client, not the user directly
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh_access_token():
    current_user_id = str(get_jwt_identity())
    role = {"role": f"{get_jwt()["role"]}"}
    
    new_access_token = create_access_token(identity = current_user_id, additional_claims = role)
    token_blocklist = create_token_blocklist(new_access_token)
    db.session.add(token_blocklist)
    db.session.commit()
    return jsonify(access_token = new_access_token), 200