import http

from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort, reqparse

from core.permissions import is_admin_permissions
from db.postgres import db
from models import Role
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "name", trim=True, type=str, help="This field cannot be blank", required=True
)


def return_or_abort_if_role_not_exist(role_id: str) -> Role:
    role = Role.find_by_role_id(role_id=role_id)
    if not role:
        message: dict = {"message": f"Role '{role_id}' doesn't exist"}
        abort(http_status_code=http.HTTPStatus.NOT_FOUND, message=message)
    return role


class RoleDetail(Resource):
    @api_response_wrapper()
    @jwt_required()
    # @is_admin_permissions()
    def get(self, role_id):
        from schemas.role import role_schema

        role = return_or_abort_if_role_not_exist(role_id=role_id)
        return role_schema.dump(role), http.HTTPStatus.OK

    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def patch(self, role_id):
        from schemas.role import role_schema

        new_name: str = parser.parse_args().get("name")
        if Role.by_name_exist(role_name=new_name):
            return {"message": f"Role '{role_id}' already exist"}, http.HTTPStatus.BAD_REQUEST
        else:
            role = return_or_abort_if_role_not_exist(role_id=role_id)
            role.name = new_name
            role.save_to_db()
            return role_schema.dump(role), http.HTTPStatus.OK

    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def delete(self, role_id: str):
        role = return_or_abort_if_role_not_exist(role_id=role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return {"message": f"Role '{role_id}' has been deleted"}, http.HTTPStatus.ACCEPTED
