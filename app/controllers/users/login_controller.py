from app.services.users.login_service import LoginService
from app.utils.responses import build_success_response
from app.utils.custom_exceptions import NoDataError
from app.schemas.user_schema import UserSchema
from flask import jsonify

class LoginController:
    def __init__(self, service: LoginService):
        self.service = service
        self.schema = UserSchema()
        
    def login(self, data):
        if not data:
            raise NoDataError()
        
        username = data["username"]
        password = data["password"]
        
        tokens = self.service.login(username, password)
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