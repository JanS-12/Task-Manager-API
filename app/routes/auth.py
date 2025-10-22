from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.schemas.user_schema import UserSchema
from app.models.user import User
from app.utils.security import hash_password, check_password
from flask_jwt_extended import create_access_token, create_refresh_token


auth_bp = Blueprint("auth", __name__, url_prefix = "/api/v1/auth")

user_schema = UserSchema()
# user_public_schema = UserSchema(exclude = ("password_hash"))

# GET --> /api/v1/auth/health
@auth_bp.route("/health", methods=["GET"])
@limiter.limit("20 per minute") # # TODO: Remember to change this back to 10
def health_check():
    return jsonify(message = "Auth reachable!")

# Register --> POST /api/v1/auth/register
@auth_bp.route("/register", methods=["POST"])
@limiter.limit("20 per minute") # TODO: Remember to change this back to 10
def register():
    json_data = request.get_json()
    # Check for input
    if not json_data:
        return jsonify(message = "No data provided."), 400
    
    # Validate Input
    errors = user_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    
    # Deserialize data
    data = user_schema.load(json_data)
    
    # If user exists
    if User.query.filter_by(username = data["username"], email = data["email"]).first():
        return jsonify(message = "User already exist"), 409
    
    new_user = User(
        username = data["username"], 
        email = data["email"], 
        password_hash = hash_password(data["password_hash"]), # .decode("utf-8") --> to convert from bytes to str for DB
        role = data["role"]
    ) 
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201

# Login --> POST "/api/v1/auth/login"
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("100 per minute") # TODO: Remember to uncomment and change this back to 10
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify(message = "No data provided"), 400
    
    username = json_data.get("username")
    password = json_data.get("password_hash")
    
    user = User.query.filter_by(username = username).first()    
    
    if not user or not check_password(password, user.password_hash):
        return jsonify(message = "Invalid credentials"), 401
    
    additional_claims = {"role": user.role}
    access_token = create_access_token(
        identity = str(user.user_id), 
        additional_claims = additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity = str(user.user_id), 
        additional_claims = additional_claims
    )
    return jsonify(access_token = access_token, refresh_token = refresh_token), 200
        
        