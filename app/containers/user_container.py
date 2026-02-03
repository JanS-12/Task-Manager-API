from app.controllers.users.profile_controller import GetUserProfileController, GetAllUserProfileController
from app.controllers.users.registration_controller import RegistrationController
from app.services.users.profile_service import GetUserProfileService, GetAllUsersProfileService
from app.services.users.registration_service import RegistrationService
from app.services.users.login_service import LoginService
from app.controllers.users.login_controller import LoginController
from app.controllers.users.logout_controller import LogoutController
from app.services.users.logout_service import LogoutService
from app.controllers.users.update_controller import UpdateUserController
from app.services.users.update_service import UpdateUserService
from app.controllers.users.remove_controller import RemoveUserController
from app.services.users.remove_service import RemoveUserService

# Old
from app.services.task_service import TaskService
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.project_service import ProjectService

# Repos
from app.repositories.project_repo import ProjectRepository
from app.repositories.token_repo import TokenRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.user_repo import UserRepository

class User_DI:
    user_repository = None
    token_repository = None
    project_repository = None
    task_repository = None
    
    auth_service = None
    user_service = None
    project_service = None
    task_service = None
    
    # New -> SRP and OCP -- Services and Controllers
    user_profile_service = None
    user_profile_controller = None
    
    users_profile_service = None
    users_profile_controller = None
    
    registration_service = None
    registration_controller = None
    
    login_service = None
    login_controller = None
    
    logout_service = None
    logout_controller = None
    
    update_service = None
    update_controller = None
    
    remove_service = None
    remove_controller = None
    
    def register_user_dependencies():
        User_DI.token_repository = TokenRepository()
        User_DI.user_repository = UserRepository()
        User_DI.project_repository = ProjectRepository()
        User_DI.task_repository = TaskRepository()
        
        
        User_DI.user_service = UserService(User_DI.user_repository)
        User_DI.auth_service = AuthService(User_DI.token_repository, User_DI.user_service)
        User_DI.project_service = ProjectService(User_DI.user_service, User_DI.project_repository)
        User_DI.task_service = TaskService(User_DI.task_repository, User_DI.project_service, User_DI.user_service)
        
        # New SRP and OCP (Workflows)
        User_DI.user_profile_service = GetUserProfileService(User_DI.user_repository)
        User_DI.user_profile_controller = GetUserProfileController(User_DI.user_profile_service)
        
        User_DI.users_profile_service = GetAllUsersProfileService(User_DI.user_repository)
        User_DI.users_profile_controller = GetAllUserProfileController(User_DI.users_profile_service)
        
        User_DI.registration_service = RegistrationService(User_DI.user_repository)
        User_DI.registration_controller = RegistrationController(User_DI.registration_service)
        
        User_DI.login_service = LoginService(User_DI.token_repository, User_DI.user_repository)
        User_DI.login_controller = LoginController(User_DI.login_service)
        
        User_DI.logout_service = LogoutService(User_DI.user_repository, User_DI.token_repository)
        User_DI.logout_controller = LogoutController(User_DI.logout_service)
        
        User_DI.update_service = UpdateUserService(User_DI.user_repository)
        User_DI.update_controller = UpdateUserController(User_DI.update_service)
        
        User_DI.remove_service = RemoveUserService(User_DI.user_repository, User_DI.token_repository)
        User_DI.remove_controller = RemoveUserController(User_DI.remove_service)
    