from app.services.users.remove_service import RemoveUserService

class RemoveUserController:
    def __init__(self, service: RemoveUserService):
        self.service = service
        
    def remove(self, user_id, requester_id):
        self.service.remove(user_id, requester_id)
        return "", 204