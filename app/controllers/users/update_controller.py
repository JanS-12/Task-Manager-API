from app.services.users.update_service import UpdateUserService
from app.utils.responses import build_success_response
from app.utils.custom_exceptions import NoDataError
from app.schemas.user_schema import UserSchema
from flask import jsonify
class UpdateUserController:
    def __init__(self, service: UpdateUserService):
        self.service = service
        self.schema = UserSchema()
    
    def update(self, user_id, requester_id, data):
        if not data:
            raise NoDataError()
        
        valid_data = self.schema.load(data)
        user = self.service.update(user_id, requester_id, valid_data)
        return jsonify(
            build_success_response(
                "User Updated Successfully",
                200, 
                self.schema.dump(user)
            )
        ), 200