from app.services.users.login_service import LoginService
from app.utils.responses import build_success_response
from app.schemas.users.user_response_schema import UserResponseSchema
from app.schemas.auth.login_schema import LoginSchema
from flask import jsonify

class LoginController:
    def __init__(self, service: LoginService):
        self.service = service
        self.login_schema = LoginSchema()
        self.schema = UserResponseSchema()
        
    def login(self, data):
        validated = self.login_schema.load(data)
        
        tokens = self.service.login(**validated)
        return jsonify(
            build_success_response(
                "Login Successful",
                200, 
                {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"]
                }
            )
        ), 200