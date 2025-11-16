from app.utils.custom_exceptions import UserNotFound, AccessDenied, NoDataError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.utils.security import hash_password, role_required
from app.models.token_blocklist import TokenBlocklist
from app.schemas.user_schema import UserSchema
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from datetime import datetime

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
    if users:       # Get all users
        return users_schema.jsonify(users), 200

    raise UserNotFound()  
 
 # GET /user_id --> Get user profile
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required(["user", "admin"])
def get_user(user_id: int):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    # Check ownership
    if claims["role"] == "admin" or user_id == current_user_id: 
        user = User.query.filter_by(id = user_id).first()
        if not user:
            raise UserNotFound()
        
        return user_schema.jsonify(user), 200
    
    raise AccessDenied()

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
        raise NoDataError()
    
    # Check if user exists
    user = User.query.filter_by(id = user_id).first()
    if not user:
        raise UserNotFound()
    
    if claims["role"] == "admin" or user_id == current_user_id:    
        # Deserialize data
        data = user_schema.load(json_data)
        
        user.username = data["username"]
        user.email = data["email"]
        user.password = hash_password(data["password"])
        user.role  = data["role"]
        db.session.commit()                 # Commit changes to db
        return user_schema.jsonify(user), 200
    
    raise AccessDenied()

# It is only logging out the current token, but it works. 
@user_bp.route("/logout", methods=["POST"])
@jwt_required()
@role_required(["user", "admin"])
def logout():
    current_user_id = int(get_jwt_identity())
    jti = get_jwt()["jti"]

    # If user exists
    user = User.query.filter_by(id = current_user_id).first()
    if not user:
        raise UserNotFound()
    
    # Get all active tokens for the user, both access and refresh
    tokens = TokenBlocklist.query.filter_by(user_id = current_user_id, revoked_at=None).all()
    if tokens:
        for token in tokens:
            token.revoked_at = datetime.now()
    else:
        # Edge case, JWT was not saved
        token = TokenBlocklist(jti = jti, user_id = current_user_id, token_type = get_jwt().get("type", "access"), revoked_at = datetime.now())
        db.session.add(token)
        
    db.session.commit()
    return jsonify(message = "User succesfully logged out!"), 200


# DELETE /<user_id> --> Delete a user    
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required(verify_type = False)
@role_required(["admin"])
def remove_user(user_id: int):   
    claims = get_jwt()
    
    if claims["role"] != "admin":
        raise AccessDenied()
    
    user = User.query.filter_by(id = user_id).first()
    if not user:
        raise UserNotFound()
    
    try:    # Transaction Block
        # Before deletion, mark revoked_at time for all active tokens
        TokenBlocklist.query.filter_by(user_id = user_id, revoked_at = None).update(
            {"revoked_at": datetime.now()}, 
            synchronize_session = False
        )
            
        # Success --> Transaction Committed
        db.session.delete(user)        
        db.session.commit()
        return jsonify(message = ""), 204 
    except Exception as e:
        # Failure --> Transaction Aborted, rollback automatically, but just to be sure we call it
        db.session.rollback()
        return jsonify(message = f"Error deleting user: {str(e)}"), 500
    