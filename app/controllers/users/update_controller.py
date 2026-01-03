from app.services.users.update_service import UpdateUserService
from app.schemas.user_schema import UserSchema
from app.utils.custom_exceptions import NoDataError

class UpdateUserController:
    def __init__(self, service: UpdateUserService):
        self.service = service
        self.schema = UserSchema()
    
    def update(self, user_id, requester_id, data):
        if not data:
            raise NoDataError()
        
        valid_data = self.schema.load(data)
        user = self.service.update(user_id, requester_id, valid_data)
        return self.schema.jsonify(user), 200