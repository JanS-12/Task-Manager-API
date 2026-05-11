from app.services.users.registration_service import RegistrationService
from app.utils.responses import build_success_response
from app.utils.custom_exceptions import NoDataError
from app.schemas.user_schema import UserSchema
from flask import jsonify
class RegistrationController:
    def __init__(self, service: RegistrationService):
        self.service = service
        self.schema = UserSchema()
        
    def register(self, json_data):
        if not json_data:
            raise NoDataError()
        
        user_data = self.schema.load(json_data) # Passed in arg in JSON format already
        user = self.service.create_profile(user_data)
        return jsonify(
            build_success_response(
                "Registration Successful",
                201, 
                self.schema.dump(user)
            )
        ), 201
        