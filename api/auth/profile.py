from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from core import config
from db.postgres import db
from db.redis import redis_db
from models.auth_models import User
from utils import codes
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "username", type=str, help="This field cannot be blank", trim=True, required=True
)


class Profile(Resource):
    @api_response_wrapper()
    @jwt_required()
    def get(self):
        from schemas.user import user_schema

        user_id: str = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user_schema.dump(user)
        return {"message": codes.OBJECT_NOT_FOUND}, 404

    @api_response_wrapper()
    @jwt_required()
    def patch(self):
        from schemas.user import user_schema

        data = parser.parse_args()
        user_id: str = get_jwt_identity()
        new_username: str = data.get("username")
        if not new_username:
            return {
                "message": "Something went wrong",
                "username": "This field cannot be blank",
            }, 400
        try:
            profile = User.query.filter_by(id=user_id).first()
            profile.username = new_username
            profile.save_to_db()
            return user_schema.dump(profile)
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, 400

    @api_response_wrapper()
    @jwt_required()
    def delete(self):
        jti: str = get_jwt().get("jti")
        user_id: str = get_jwt_identity()
        try:
            profile = User.query.filter_by(id=user_id).first()
            db.session.delete(profile)
            db.session.commit()
            """ revoke token """
            redis_db.add_token(
                key=jti, expire=config.JWT_ACCESS_TOKEN_EXPIRES, value=user_id
            )
            return {"message": "success deleted"}
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, 400


class GetSuccessHistory(Resource):
    @api_response_wrapper()
    @jwt_required()
    def get(self) -> str:
        return redis_db.get_access_history(user_id=get_jwt_identity())
