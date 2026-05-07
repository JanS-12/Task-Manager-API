from app.utils.custom_exceptions import AppException
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from ..utils.logging import get_logger, log_error
from datetime import datetime
from flask import jsonify, request, has_request_context
from logging import WARNING, ERROR

error_logger = get_logger("error")

def register_error_handlers(app):
    
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        log_error(
            error_logger,
            WARNING,
            message = e.message,
            error_type = e.__class__.__name__,
            status_code = e.status_code
        )

        return jsonify(
            build_error_response(
                e.__class__.__name__,
                e.message,
                e.status_code
            )
        ), e.status_code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        log_error(
            error_logger,
            WARNING,
            message = "Unprocessable Entity",
            error_type = "ValidationError",
            status_code = 422
        )

        return jsonify(
            build_error_response(
                "ValidationError",
                "Unprocessable Entity",
                422
            )
        ), 422

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        log_error(
            error_logger,
            WARNING,
            message = str(e),
            error_type = e.__class__.__name__,
            status_code = e.code
        )

        return jsonify(
            build_error_response(
                e.__class__.__name__,
                str(e),
                e.code
            )
        ), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        log_error(
            error_logger,
            ERROR,
            message = str(e),
            error_type = e.__class__.__name__,
            status_code = 500
        )

        return jsonify(
            build_error_response(
                "InternalServerError",
                "An unexpected error occurred",
                500
            )
        ), 500
    
    
    
def build_error_response(error_type, message, status_code, details=None):
    return {
        "error": {
            "type": error_type,
            "message": message,
            "status_code": status_code,
            "path": request.path if has_request_context() else None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "details": details or {}
        }
    }