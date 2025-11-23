from .logging import get_logger
from flask import request

error_logger = get_logger("error")
class AppException(Exception):
    """Base class for all custom application exceptions."""
    status_code = 400
    error = "Application Error"

    def __init__(self, message=None, status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.message = message or self.error

    def to_dict(self):
        return {
            "error": self.error,
            "message": self.message,
            "status_code": self.status_code
        }

# --- Specific subclasses --- #
# --- General Exceptions --- #
class BadRequest(AppException):
    error = "Bad Request"
    status_code = 400

class Unauthorized(AppException):
    error = "Unauthorized"
    status_code = 401

class Forbidden(AppException):
    error = "Forbidden"
    status_code = 403

class ResourceNotFound(AppException):
    error = "Resource Not Found"
    status_code = 404

class ConflictError(AppException):
    error = "Conflict"
    status_code = 409

# --- Auth Errors --- #
class NoDataError(BadRequest):
    def __init__(self):
        super().__init__("No data provided.")
        error_logger.warning("Bad Request", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "No Data Error",
            "status_code": 400
        })

class InvalidCredentialsError(Unauthorized):
    def __init__(self):
        super().__init__("Invalid username or password.")
        error_logger.warning("Unauthorized", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "Invalid Credentials Error",
            "status_code": 401
        })
        
class ExistingCredentialsError(ConflictError):
    def __init__(self):
        super().__init__("This username or password already exists.")
        error_logger.warning("Conflict Error", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "Existing Credentials Error",
            "status_code": 409
        })
        
class AccessDenied(Forbidden):
    def __init__(self):
        super().__init__("Access Denied.")
        error_logger.warning("Forbidden", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "Access Denied",
            "status_code": 403
        })
    
# --- User Errors --- #
class UserNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__("User not found.")
        error_logger.warning("Resource Not Found", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "User Not Found",
            "status_code": 404
        })

# --- Project Errors --- #
class ProjectNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__("Project not found.")
        error_logger.warning("Resource Not Found", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "Project Not Found",
            "status_code": 404
        })
        
# --- Task Errors --- #
class TaskNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__("Task not found.")
        error_logger.warning("Resource Not Found", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "Task Not Found",
            "status_code": 404
        })

class TaskIncorrectProject(Forbidden):
    def __init__(self):
        super().__init__("The task does not belong to the specified project.")
        error_logger.warning("Forbidden", extra = {
            "path": request.path,
            "client_ip": request.remote_addr,
            "error_type": "Task Incorrect Project",
            "status_code": 403
        })