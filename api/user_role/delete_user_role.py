from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from core.permissions import is_admin_permissions
from db.postgres import db
from models import UserRole
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "user_id", trim=True, type=str, help="send correct id", required=True
)
parser.add_argument(
    "role_id", trim=True, type=str, help="send correct id", required=True
)


class DeleteUserRole(Resource):
    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def delete(self):
        data = parser.parse_args()
        user_id: str = data.get("user_id")
        role_id: str = data.get("role_id")
        if user_id == get_jwt_identity():
            return {
                "message": "wrong data",
                "description": "You can not delete own role",
            }, 400
        """ delete user's role """
        user_role = UserRole.get_row_by_ids(user_id=user_id, role_id=role_id)
        if user_role:
            db.session.delete(user_role)
            db.session.commit()
        return {}
