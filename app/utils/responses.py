from flask import request, has_request_context
from datetime import datetime, timezone

def build_error_response(error_type, message, status_code, details = None):
    return {
        "error": {
            "type": error_type,
            "message": message,
            "status_code": status_code,
            "path": request.path if has_request_context() else None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {}
        }
    }
    
def build_success_response(message, status_code, data = None):
    return {
        "success": {
            "message": message,
            "status_code": status_code,
            "path": request.path if has_request_context() else None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
    }