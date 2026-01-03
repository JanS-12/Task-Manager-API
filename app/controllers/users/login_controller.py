from app.services.users.login_service import LoginService
from app.utils.custom_exceptions import NoDataError
from app.schemas.user_schema import UserSchema

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
        return tokens