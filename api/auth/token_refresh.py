import http

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource

from db.redis import redis_db
from utils.decorators import api_response_wrapper


class TokenRefresh(Resource):
    @api_response_wrapper()
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt().get("jti")
        user_id: str = get_jwt_identity()
        if redis_db.is_jti_blacklisted(jti=jti):
            return {
                "access_token": create_access_token(identity=user_id)
            }, http.HTTPStatus.OK
        return {
            "message": "token revoked",
            "description": "The refresh token has been revoked.",
        }, http.HTTPStatus.UNAUTHORIZED
