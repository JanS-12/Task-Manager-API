from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from app.utils.custom_exceptions import AppException

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify(error="Input validation failed", message=e.messages), 400
    
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