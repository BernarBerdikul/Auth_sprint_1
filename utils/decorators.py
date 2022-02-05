from functools import wraps
from typing import Optional

from flask_restful import abort


def param_error_handler():
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                message: dict = {
                    "message": "Wrong params",
                    "description": "Check that you send correct data",
                    "errors": [],
                }
                abort(http_status_code=400, message=message)

        return inner

    return decorator


def api_response_wrapper():
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs) -> tuple:
            result = func(*args, **kwargs)

            response, status_code = (
                result if isinstance(result, tuple) else (result, 200)
            )

            message: Optional[str] = (
                response.pop("message") if "message" in response else None
            )
            description: Optional[str] = (
                response.pop("description") if "description" in response else None
            )
            errors: Optional[list] = (
                response.pop("errors") if "errors" in response else []
            )
            """ prepare wrapped response """
            data: list = []
            if isinstance(response, list):
                data = response
            elif response:
                data.append(response)
            wrapped_response: dict = {
                "success": True if str(status_code).startswith("2") else False,
                "data": data,
            }
            if message:
                wrapped_response["message"] = message
            if description:
                wrapped_response["description"] = description
            if errors:
                wrapped_response["errors"] = errors
            return wrapped_response, status_code

        return inner

    return decorator
