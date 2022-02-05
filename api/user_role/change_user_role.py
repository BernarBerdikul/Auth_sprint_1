from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from core.permissions import is_admin_permissions
from models import UserRole
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "user_id", trim=True, type=str, help="send correct id", required=True
)
parser.add_argument(
    "role_id", trim=True, type=str, help="send correct id", required=True
)


class ChangeUserRole(Resource):
    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def post(self):
        data = parser.parse_args()
        user_id: str = data.get("user_id")
        role_id: str = data.get("role_id")
        if not UserRole.is_row_exist(user_id=user_id, role_id=role_id):
            new_user_role = UserRole(user_id=user_id, role_id=role_id)
            new_user_role.save_to_db()
        return {}
