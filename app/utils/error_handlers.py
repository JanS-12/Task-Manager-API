from app.utils.custom_exceptions import AppException
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from ..utils.logging import get_logger
from flask import jsonify

error_logger = get_logger("error")

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify(error="Unprocessable Entity", message=e.messages, status_code = 422), 422
    
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        response = e.to_dict()
        return jsonify(response), e.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify(error=e.description), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        return jsonify(error="An unexpected error occurred", message=str(e)), 500