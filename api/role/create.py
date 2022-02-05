from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from core.permissions import is_admin_permissions
from models import Role
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True, trim=True
)


class RoleCreate(Resource):
    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def post(self):
        from schemas.role import role_schema

        data = parser.parse_args()
        role_name: str = data.get("name")
        if not Role.by_name_exist(role_name=role_name):
            new_role = Role(name=role_name)
            new_role.save_to_db()
            return role_schema.dump(new_role), 201
        return {
            "message": "wrong data",
            "errors": [{"name": f"Role name <{role_name}> already exist"}],
        }, 400
