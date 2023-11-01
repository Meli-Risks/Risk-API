from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt

from src.infrastructure.utils.responses import error_response


def role_required(required_roles):
    """
    A decorator that checks if the user has the required roles to access a specific functionality.

    :param required_roles: A list of role names required to access the functionality.
    :type required_roles: list

    :return: The decorated function.
    :rtype: function
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_roles = claims.get("roles", [])

            for role in required_roles:
                if role in user_roles:
                    return fn(*args, **kwargs)

            response = error_response(403, "Acceso denegado para esta funcionalidad")
            return jsonify(response), 403

        return wrapper

    return decorator
