from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.schemas.user_schema import UserSchema
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist
from app.utils.security import hash_password, check_password
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token



auth_bp = Blueprint("auth", __name__, url_prefix = "/api/v1/auth")

user_schema = UserSchema()
# user_public_schema = UserSchema(exclude = ("password"))

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
        password = hash_password(data["password"]), # .decode("utf-8") --> to convert from bytes to str for DB
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
    password = json_data.get("password")
    
    user = User.query.filter_by(username = username).first()    
    
    if not user or not check_password(password, user.password):
        return jsonify(message = "Invalid credentials"), 401
    
    additional_claims = {"role": user.role}
    access_token = create_access_token(
        identity = str(user.id), 
        additional_claims = additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity = str(user.id), 
        additional_claims = additional_claims
    )
    
    access_jti = decode_token(access_token)["jti"]
    refresh_jti = decode_token(refresh_token)["jti"]
    
    tokens_blocklist = [
        TokenBlocklist(jti = access_jti, user_id = user.id, token_type = "access", revoked_at=None),
        TokenBlocklist(jti = refresh_jti, user_id = user.id, token_type = "refresh", revoked_at=None)
    ]
    
    db.session.add_all(tokens_blocklist)
    db.session.commit()
    
    
    return jsonify(access_token = access_token, refresh_token = refresh_token), 200
        
