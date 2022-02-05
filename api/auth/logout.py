from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource

from core import config
from db.redis import redis_db
from utils.decorators import api_response_wrapper


class UserLogoutAccess(Resource):
    @api_response_wrapper()
    @jwt_required()
    def post(self):
        jti: str = get_jwt().get("jti")
        user_id: str = get_jwt_identity()
        try:
            redis_db.add_token(
                key=jti, expire=config.JWT_ACCESS_TOKEN_EXPIRES, value=user_id
            )
            return {"message": "Access token has been revoked"}
        except Exception:
            return {"message": "Something went wrong"}, 400


class UserLogoutRefresh(Resource):
    @api_response_wrapper()
    @jwt_required(refresh=True)
    def post(self):
        jti: str = get_jwt().get("jti")
        try:
            redis_db.delete_token(key=jti)
            return {"message": "Refresh token has been revoked"}
        except Exception:
            return {"message": "Something went wrong"}, 400
