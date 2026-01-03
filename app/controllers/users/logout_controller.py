from app.services.users.logout_service import LogoutService

class LogoutController:
    def __init__(self, service: LogoutService):
        self.service = service
    
    def logout(self, user_id):
        self.service.logout(user_id)
        return