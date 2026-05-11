from app.services.users.logout_service import LogoutService
from app.utils.responses import build_success_response
from flask import jsonify
class LogoutController:
    def __init__(self, service: LogoutService):
        self.service = service
    
    def logout(self, user_id):
        self.service.logout(user_id)
        return jsonify(
            build_success_response(
                "Logout Successful",
                200, 
                {}
            )
        ), 200