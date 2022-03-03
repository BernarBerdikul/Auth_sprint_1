import http

from flask_restful import Resource, reqparse

from db.postgres import db
from models import Role, User, UserRole
from utils import constants
from utils.decorators import api_response_wrapper
from utils.validators import username_validation

parser = reqparse.RequestParser()
parser.add_argument(
    "username", type=str, help="This field cannot be blank", required=True, trim=True
)
parser.add_argument(
    "password", type=str, help="This field cannot be blank", required=True, trim=True
)
parser.add_argument(
    "password_confirm",
    type=str,
    help="This field cannot be blank",
    required=True,
    trim=True,
)


class UserRegistration(Resource):
    @api_response_wrapper()
    def post(self):
        data = parser.parse_args()
        username: str = data.get("username")
        password: str = data.get("password")
        password_confirm: str = data.get("password_confirm")
        """ check username in DB """
        if User.find_by_username(username=username):
            return {
                "message": "wrong data",
                "errors": [
                    {"username": f"User {username} already exists"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        """ check that passwords are equal """
        if password != password_confirm:
            return {
                "message": "wrong data",
                "errors": [
                    {"password": "passwords are not equal"},
                    {"password_confirm": "passwords are not equal"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        """ create new user """
        new_user = User(username=username_validation(value=username))
        new_user.set_password(password=password)
        db.session.add(new_user)
        """ find default role """
        default_role = Role.find_by_role_name(
            role_name=constants.DEFAULT_ROLE_FOR_ALL_USERS
        )
        """ set default role for user """
        new_user_role = UserRole(user_id=new_user.id, role_id=default_role.id)
        db.session.add(new_user_role)
        db.session.commit()
        return {"message": f"User {username} was created"}, http.HTTPStatus.CREATED
