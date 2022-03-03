import http
import re

from flask_restful import abort

from . import codes, constants, messages


def username_validation(value: str) -> str:
    """Validate username's value for database"""
    message: dict = {
        "message": codes.INVALID_USERNAME_ERROR,
        "errors": [],
    }
    """ Check which symbols username contains """
    if not re.match(constants.REGEX_FOR_FIRST_SYMBOL, value):
        message["errors"].append({"username": messages.USERNAME_FIRST_SYMBOL})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    if not re.match(constants.REGEX_FOR_LOGIN, value):
        message["errors"].append({"username": messages.USERNAME_OTHER_SYMBOLS})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    """ Check username's length """
    if len(value) < constants.USERNAME_MIN_LENGTH:
        message["errors"].append({"username": messages.USERNAME_MIN_INVALID})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    elif len(value) > constants.USERNAME_MAX_LENGTH:
        message["errors"].append({"username": messages.USERNAME_MAX_INVALID})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    """ Return validated username """
    return value


def password_validation(value: str) -> str:
    """Validate password's value for database"""
    message: dict = {
        "message": codes.INVALID_PASSWORD_ERROR,
        "errors": [],
    }
    """ Check which symbols password contains """
    if re.match(constants.REGEX_ALPHABET_IN_PASSWORD, value):
        if not re.findall(constants.REGEX_UPPER_LATTER_IN_PASSWORD, value):
            message["errors"].append({"password": messages.PASSWORD_UPPER_LATTER})
            abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
        elif not re.findall(constants.REGEX_LOWER_LATTER_IN_PASSWORD, value):
            message["errors"].append({"password": messages.PASSWORD_LOWER_LATTER})
            abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
        elif not re.findall(constants.REGEX_PASSWORD_INT_SYMBOL, value):
            message["errors"].append({"password": messages.PASSWORD_INTEGER_SYMBOL})
            abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    else:
        message["errors"].append({"password": messages.PASSWORD_ALPHABET})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    """ Check password's length """
    if len(value) < constants.PASSWORD_MIN_LENGTH:
        message["errors"].append({"password": messages.PASSWORD_MIN_LENGTH})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    elif len(value) > constants.PASSWORD_MAX_LENGTH:
        message["errors"].append({"password": messages.PASSWORD_MAX_LENGTH})
        abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
    """ Return validated password """
    return value
