
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


class UnprocessableEntity(AppException):
    error = "Unprocessable Entity"
    status_code = 422
