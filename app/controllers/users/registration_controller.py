from app.services.users.registration_service import RegistrationService
from app.schemas.users.user_response_schema import UserResponseSchema
from app.schemas.auth.registration_schema import RegistrationSchema
from app.utils.responses import build_success_response
from flask import jsonify
class RegistrationController:
    def __init__(self, service: RegistrationService):
        self.service = service
        self.registration_schema = RegistrationSchema()
        self.response_schema = UserResponseSchema()
        
    def register(self, data):
        validated = self.registration_schema.load(data) # Passed in arg in JSON format already
        user = self.service.create_profile(validated)
        return jsonify(
            build_success_response(
                "Registration Successful",
                201, 
                self.response_schema.dump(user)
            )
        ), 201
        