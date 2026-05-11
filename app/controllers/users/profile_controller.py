from app.services.users.profile_service import GetUserProfileService, GetAllUsersProfileService
from app.utils.responses import build_success_response
from app.schemas.user_schema import UserSchema
from flask import jsonify

# These two are different worklows, 
# I just put them in the same file for simplicity,
# yet I know they belong in two separate files.
class GetUserProfileController:
    def __init__(self, service: GetUserProfileService):
        self.service = service
        self.schema = UserSchema() # DTO
        
    def get(self, user_id, requester_id):  
        user = self.service.get(user_id, requester_id)
        return jsonify(
            build_success_response(
                "User Retrieved Successfully",
                200, 
                self.schema.dump(user)
            )
        ), 200


class GetAllUserProfileController:
    def __init__(self, service: GetAllUsersProfileService):
        self.service = service
        self.schema = UserSchema(many = True) # DTO
        
    def get(self, requester_id):  
        users = self.service.get(requester_id)
        return jsonify(
            build_success_response(
                "Users Retrieved Successfully",
                200, 
                self.schema.dump(users)
            )
        ), 200