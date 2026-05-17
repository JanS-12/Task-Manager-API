from app.schemas.users.user_response_schema import UserResponseSchema
from app.schemas.users.update_user_schema import UpdateUserSchema
from app.services.users.update_service import UpdateUserService
from app.utils.responses import build_success_response
from flask import jsonify
class UpdateUserController:
    def __init__(self, service: UpdateUserService):
        self.service = service
        self.response_schema = UserResponseSchema()
        self.update_schema = UpdateUserSchema()
    
    def update(self, user_id, requester_id, data):
        validated = self.update_schema.load(data, partial = True)
        user = self.service.update(user_id, requester_id, validated)
        return jsonify(
            build_success_response(
                "User Updated Successfully",
                200, 
                self.response_schema.dump(user)
            )
        ), 200