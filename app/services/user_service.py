from app.utils.custom_exceptions import ExistingCredentialsError, UserNotFound, NoDataError, AccessDenied
from app.repositories.user_repo import UserRepository
from app.models.token_blocklist import TokenBlocklist
from app.schemas.user_schema import UserSchema
from app.utils.logging import get_logger
from datetime import datetime

auth_logger = get_logger("auth")
audit_logger = get_logger("audit")

# Handles all user business logic
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.user_schema = UserSchema()
        
    def get_user(self, user_id, requester_id):
        requester = self.user_repo.get_by_id(requester_id)
        user = self.user_repo.get_by_id(user_id)
        
        if not user or not requester:
            raise UserNotFound()
        
        if requester.role != "admin" and requester_id != user.id:
            raise AccessDenied()
        
        audit_logger.info(f"\"{user.username}\"'s profile was retrieved.")
        return user
    
    def get_all_users(self, requester_id):
        admin = self.user_repo.get_by_id(requester_id)
        # Check privileges
        if not admin:  
            raise UserNotFound("Admin not found.")
        
        if admin.role != "admin":
            raise AccessDenied("Not enough privileges to access this information.")

        users = self.user_repo.get_all_users()
        if not users:
            raise UserNotFound("Users not found.")
        
        audit_logger.info(f"Admin \"{admin.username}\" retrieved all user's profiles.")
        return users
    
    def create_user(self, data):
        # Check input
        if not data:
            raise NoDataError()
        
        # Validate and deseralize data
        user_data = self.user_schema.load(data)
        
        # Business rules go here
        if self.user_repo.get_by_email(user_data["email"]):
            raise ExistingCredentialsError()

        # Persist
        user = self.user_repo.create(user_data)
        audit_logger.info(f"New user created -> Username: \"{user.username}\", Email: \"{user.email}\".")
        return user
    
    def update_user(self, user_id, data, requester_id):
        # Business rules
        user = self.user_repo.get_by_id(user_id)
        requester = self.user_repo.get_by_id(requester_id)
        
        if not user or not requester:
            raise UserNotFound()
        
        # Check Input
        if not data:
            raise NoDataError()
        
        if requester.role != "admin" and requester.id != user.id:
            raise AccessDenied()
        
        # Validate and deseralize data
        user_data = self.user_schema.load(data)

        # Persist
        user = self.user_repo.update(user.id, user_data)
        audit_logger.info(f"User's ID \'{user.id}\' has been updated -> Username: \"{user.username}\", Email: \"{user.email}\".")        
        return user
        
    def delete_user(self, user_id, requester_id):
        user = self.user_repo.get_by_id(user_id)
        requester = self.user_repo.get_by_id(requester_id)
        
        if not user or not requester:
            raise UserNotFound()

        # A user cannot delete themselves, nor cannot delete a user unless admin
        if user.id == requester.id or requester.role != "admin":
            raise AccessDenied()
        
        # Before deletion, mark revoked_at time for all active tokens
        # Inject later TokenBlocklist service later
        TokenBlocklist.query.filter_by(user_id = user.id, revoked_at = None).update(
            {"revoked_at": datetime.now()}, 
            synchronize_session = False
        )
        auth_logger.info(f"All active tokens for user \"{user.username}\" were revoked.")
        
        message = self.user_repo.delete(user.id)
        audit_logger.info(f"User that had ID \'{user_id}\' has been removed.")
        # Don't return anything for now         
        
    # The next functions are to be used and called by the AuthService ONLY 
    # For authentication purposes 
    def get_user_by_username(self, username):
        if not username:
            raise NoDataError()

        user = self.user_repo.get_by_username(username)
        
        return user
    
    def get_user_by_email(self, email):
        if not email:
            raise NoDataError()

        user = self.user_repo.get_by_email(email)
        return user