import http

import click
from flasgger import Swagger
from flask import Flask
from flask.cli import with_appcontext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api

import core.config
from core import config
from db import cache, db, db_url
from models import Role, User, UserRole
from utils import constants
from utils.decorators import requires_basic_auth

app = Flask(__name__)
api = Api(app=app)
migrate = Migrate(app, db)
ma = Marshmallow(app=app)

swagger = Swagger(
    app,
    decorators=[requires_basic_auth],
    template={
        "swagger": "2.0",
        "info": {
            "title": "Auth service",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },
)

app.config["SQLALCHEMY_DATABASE_URI"]: str = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: bool = False

db.init_app(app=app)

app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY  # Change this!
app.config["JWT_COOKIE_SECURE"] = config.JWT_COOKIE_SECURE
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT_REFRESH_TOKEN_EXPIRES
app.config["JWT_BLACKLIST_ENABLED"] = config.JWT_BLACKLIST_ENABLED
app.config["JWT_BLACKLIST_TOKEN_CHECKS"]: list = ["access", "refresh"]
app.config["TESTING"]: bool = config.TESTING
app.config["JWT_COOKIE_CSRF_PROTECT"]: bool = False if config.TESTING else True
app.config["SWAGGER"] = {
    "title": "Swagger JWT Authentiation App",
    "uiversion": 3,
}

jwt = JWTManager(app)


# TODO: Delete it
@app.cli.command("create_admin")
@with_appcontext
@click.argument("username")
@click.argument("password")
def create_admin(username: str, password: str):
    """create new user with admin role"""
    if core.config.TESTING:
        new_user = User(username=username)
        new_user.set_password(password=password)
        db.session.add(new_user)
        """ find admin role """
        role_admin = Role.find_by_role_name(role_name=constants.ROLE_FOR_ADMIN)
        """ set admin role for user """
        new_user_role = UserRole(user_id=new_user.id, role_id=role_admin.id)
        db.session.add(new_user_role)
        db.session.commit()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload) -> bool:
    access = jwt_payload.get("type")
    if access == "access":
        return cache.is_jti_blacklisted(jwt_payload.get("jti"))
    else:
        # In blacklist there are only access tokens
        return False


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """we have to keep the argument here, since it's passed
    in by the caller internally"""
    data: dict = {
        "success": False,
        "message": "invalid_token",
        "description": "Signature verification failed.",
        "errors": [],
    }
    return data, http.HTTPStatus.UNAUTHORIZED


@jwt.unauthorized_loader
def missing_token_callback(error):
    data: dict = {
        "success": False,
        "message": "authorization_required",
        "description": "Request does not contain an access token.",
        "errors": [],
    }
    return data, http.HTTPStatus.UNAUTHORIZED


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    data: dict = {
        "success": False,
        "message": "fresh_token_required",
        "description": "The token is not fresh.",
        "errors": [],
    }
    return data, http.HTTPStatus.UNAUTHORIZED


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    data: dict = {
        "success": False,
        "message": "token_revoked",
        "description": "The token has been revoked.",
        "errors": [],
    }
    return data, http.HTTPStatus.UNAUTHORIZED


@app.before_first_request
def create_tables():
    # db.create_all()
    if not Role.by_name_exist(role_name=constants.DEFAULT_ROLE_FOR_ALL_USERS):
        new_role = Role(name=constants.DEFAULT_ROLE_FOR_ALL_USERS)
        new_role.save_to_db()
    if not Role.by_name_exist(role_name=constants.ROLE_FOR_ADMIN):
        new_role = Role(name=constants.ROLE_FOR_ADMIN)
        new_role.save_to_db()


def create_app(flask_app):
    db.init_app(app=flask_app)
    from api.auth import api_bp_auth
    from api.role import api_bp_role
    from api.user_role import api_bp_user_role
    app.register_blueprint(api_bp_auth)
    app.register_blueprint(api_bp_role)
    app.register_blueprint(api_bp_user_role)
    # flask_app.run(debug=True)
    flask_app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    create_app(flask_app=app)
