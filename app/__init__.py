from .controllers.users.profile_controller import GetUserProfileController, GetAllUserProfileController
from .controllers.users.registration_controller import RegistrationController
from .services.users.profile_service import GetUserProfileService, GetAllUsersProfileService
from .services.users.registration_service import RegistrationService
from .services.users.login_service import LoginService
from .controllers.users.login_controller import LoginController
from .controllers.users.logout_controller import LogoutController
from .services.users.logout_service import LogoutService
from .controllers.users.update_controller import UpdateUserController
from .services.users.update_service import UpdateUserService
from .controllers.users.remove_controller import RemoveUserController
from .services.users.remove_service import RemoveUserService

from .routes import user_bp, project_bp, task_bp, auth_bp
from .utils.error_handlers import register_error_handlers
from .repositories.project_repo import ProjectRepository
from .repositories.token_repo import TokenRepository
from .services.project_service import ProjectService
from .repositories.task_repo import TaskRepository
from .repositories.user_repo import UserRepository
from .models.token_blocklist import TokenBlocklist
from .services.task_service import TaskService
from .services.auth_service import AuthService
from .services.user_service import UserService

from .extensions import db, ma, jwt, limiter
from .utils.seed import seed_data
from .containers.user_container import DI
from flask import Flask
import logging.config
import yaml

def create_app(config_name = "default"):
    app = Flask(__name__)
    
    # Double Check Config
    if config_name == "testing":
        app.config.from_object("app.config.config.TestingConfig")
    else:
        app.config.from_object("app.config.config.Config")
        
    # Load Logging Config
    config_path = "app/config/logging.yaml"
    with open(config_path, "r") as file:
        log_config = yaml.safe_load(file)
        logging.config.dictConfig(log_config)
    
    logger = logging.getLogger("app")
    logger.info("Starting application with config: %s", config_name)

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    logger.info("Initializing Extensions")
    
    # Register DI Wiring
    DI.token_repository = TokenRepository()
    DI.user_repository = UserRepository()
    DI.project_repository = ProjectRepository()
    DI.task_repository = TaskRepository()
    
    
    DI.user_service = UserService(DI.user_repository)
    DI.auth_service = AuthService(DI.token_repository, DI.user_service)
    DI.project_service = ProjectService(DI.user_service, DI.project_repository)
    DI.task_service = TaskService(DI.task_repository, DI.project_service, DI.user_service)
    
    # New SRP and OCP (Workflows)
    DI.user_profile_service = GetUserProfileService(DI.user_repository)
    DI.user_profile_controller = GetUserProfileController(DI.user_profile_service)
    
    DI.users_profile_service = GetAllUsersProfileService(DI.user_repository)
    DI.users_profile_controller = GetAllUserProfileController(DI.users_profile_service)
    
    DI.registration_service = RegistrationService(DI.user_repository)
    DI.registration_controller = RegistrationController(DI.registration_service)
    
    DI.login_service = LoginService(DI.token_repository, DI.user_repository)
    DI.login_controller = LoginController(DI.login_service)
    
    DI.logout_service = LogoutService(DI.user_repository, DI.token_repository)
    DI.logout_controller = LogoutController(DI.logout_service)
    
    DI.update_service = UpdateUserService(DI.user_repository)
    DI.update_controller = UpdateUserController(DI.update_service)
    
    DI.remove_service = RemoveUserService(DI.user_repository, DI.token_repository)
    DI.remove_controller = RemoveUserController(DI.remove_service)
    
    # Create tables
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()
        logger.info("Database Seeded Succesfully")

    # Register blueprints
    logger.info("Registering Blueprints")
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)
    
    # Register error handlers
    logger.info("Registering Error Handlers")
    register_error_handlers(app)
    logger.info("App Created Succesfully!")
    return app  

@jwt.token_in_blocklist_loader  # Check for revoked tokens automatically
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload.get("jti")
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    
    if token.revoked_at is not None:
        logging.getLogger("auth").info(f"Token with jti {jti} was revoked at time: {token.revoked_at}")
    
    # if token exists and revoked_at is set -> revoked
    return token is not None and token.revoked_at is not None