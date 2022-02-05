from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models import Role
from utils.decorators import api_response_wrapper


class RoleList(Resource):
    @api_response_wrapper()
    @jwt_required()
    # @is_admin_permissions()
    def get(self) -> dict:
        from schemas.role import roles_schema

        return {"roles": roles_schema.dump(Role.query.all())}
