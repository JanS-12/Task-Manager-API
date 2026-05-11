from app.services.users.refresh_access_token import RefreshAccessTokenService 
from app.utils.responses import build_success_response
from app.utils.custom_exceptions import NoDataError
from flask import jsonify
class RefreshAccessTokenController:
    def __init__(self, service: RefreshAccessTokenService):
        self.service = service

    def refresh_access_token(self, user_id):
        if not user_id:
            raise NoDataError()
        
        new_access_token = self.service.refresh_access_token(user_id)
        return jsonify(
            build_success_response(
                "New Access Token Issued",
                200,
                {"access_token": new_access_token}
            )
        ), 200