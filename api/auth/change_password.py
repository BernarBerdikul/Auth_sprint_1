import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from db.postgres import db
from models import User
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument("password", help="This field cannot be blank", required=True)


class ChangePassword(Resource):
    @api_response_wrapper()
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        password: str = data.get("password")
        user_id: str = get_jwt_identity()
        try:
            current_user = User.query.filter_by(id=user_id).first()
            current_user.set_password(password=password)
            current_user.save_to_db()
            return {
                "message": "Successful password change by the user"
            }, http.HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST
