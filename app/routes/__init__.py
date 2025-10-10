from .users import  user_bp
from .projects import project_bp
from .tasks import task_bp
from .auth import auth_bp

__all__ = ["user_bp", "project_bp", "task_bp", "auth_bp"]
