import logging
from flask import request, has_request_context

def get_logger(name):
    return logging.getLogger(name)

def log_error(logger, level, message, error_type=None, status_code=None, details=None):
    extra = {}

    if has_request_context():
        extra.update({
            "path": request.path,
            "method": request.method,
            "client_ip": request.remote_addr
        })

    if error_type:
        extra["error_type"] = error_type

    if status_code:
        extra["status_code"] = status_code

    if details:
        extra["details"] = details

    logger.log(level, message, extra=extra)