from app.services.users.profile_service import GetUserProfileService, GetAllUsersProfileService
from app.services.users.refresh_access_token import RefreshAccessTokenService
from app.services.users.registration_service import RegistrationService
from app.services.users.update_service import UpdateUserService
from app.services.users.remove_service import RemoveUserService
from app.services.users.logout_service import LogoutService
from app.services.users.login_service import LoginService

from app.controllers.users.profile_controller import GetUserProfileController, GetAllUserProfileController
from app.controllers.users.refresh_access_token import RefreshAccessTokenController
from app.controllers.users.registration_controller import RegistrationController
from app.controllers.users.update_controller import UpdateUserController
from app.controllers.users.remove_controller import RemoveUserController
from app.controllers.users.logout_controller import LogoutController
from app.controllers.users.login_controller import LoginController

from app.repositories.project_repo import ProjectRepository
from app.repositories.token_repo import TokenRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.user_repo import UserRepository

class UserContainer:
    def __init__(
        self,
        user_repository=None,
        token_repository=None,
        project_repository=None,
        task_repository=None,
    ):
        # Dependencies (can be overridden in tests)
        self.user_repository = user_repository or UserRepository()
        self.token_repository = token_repository or TokenRepository()
        self.project_repository = project_repository or ProjectRepository()
        self.task_repository = task_repository or TaskRepository()

        # Services
        self.user_profile_service = GetUserProfileService(self.user_repository)
        self.users_profile_service = GetAllUsersProfileService(self.user_repository)
        self.registration_service = RegistrationService(self.user_repository)
        self.login_service = LoginService(self.token_repository, self.user_repository)
        self.logout_service = LogoutService(self.user_repository, self.token_repository)
        self.update_service = UpdateUserService(self.user_repository)
        self.remove_service = RemoveUserService(self.user_repository, self.token_repository)
        self.refresh_access_token_service = RefreshAccessTokenService(
            self.token_repository, self.user_repository
        )

        # Controllers
        self.user_profile_controller = GetUserProfileController(self.user_profile_service)
        self.users_profile_controller = GetAllUserProfileController(self.users_profile_service)
        self.registration_controller = RegistrationController(self.registration_service)
        self.login_controller = LoginController(self.login_service)
        self.logout_controller = LogoutController(self.logout_service)
        self.update_controller = UpdateUserController(self.update_service)
        self.remove_controller = RemoveUserController(self.remove_service)
        self.refresh_access_token_controller = RefreshAccessTokenController(
            self.refresh_access_token_service
        )