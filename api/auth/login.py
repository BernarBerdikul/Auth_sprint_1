from datetime import datetime
from typing import Any, Union

import jwt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

from core import config
from db.redis import redis_db
from models import User
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument("username", help="This field cannot be blank", required=True)
parser.add_argument("password", help="This field cannot be blank", required=True)


class UserLogin(Resource):
    @api_response_wrapper()
    def post(self):
        data = parser.parse_args()
        username: str = data.get("username", "")
        current_user = User.find_by_username(username=username)
        if not current_user:
            return {"message": f"User {data.get('username')} doesn't exist"}, 404

        if current_user.check_password(password=data.get("password")):
            acc_token: str = create_access_token(identity=current_user.id)
            ref_token: str = create_refresh_token(identity=current_user.id)
            """ "put refresh token in REDIS" """
            jti: Union[str, Any] = jwt.decode(
                jwt=ref_token, key=config.JWT_SECRET_KEY, algorithms="HS256"
            ).get("jti")
            """ add refresh token in black list """
            redis_db.add_token(
                key=jti, expire=config.JWT_REFRESH_TOKEN_EXPIRES, value=current_user.id
            )
            """ save history """
            redis_db.save_access_history(
                user_id=current_user.id,
                access_history=(
                    f"устройство: {request.user_agent.string} "
                    f"дата входа: {datetime.now()}"
                ),
            )
            return {
                "message": f"Logged in as {current_user.username}",
                "access_token": acc_token,
                "refresh_token": ref_token,
            }
        return {"message": "Wrong credentials"}, 400
