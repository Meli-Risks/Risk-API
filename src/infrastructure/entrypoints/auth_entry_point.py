from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token

from src.application.app import jwt
from src.domain.usecases.auth_use_case import AuthUseCase
from src.infrastructure.entrypoints import auth_gateway, blacklist_gateway

bp = Blueprint('auth', __name__)

auth_use_case = AuthUseCase(auth_gateway, blacklist_gateway)


@bp.route('/api/v1/login', methods=['POST'])
def login():
    """
    Authenticates a user and returns access and refresh tokens.

    :return: A dictionary containing access and refresh tokens.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    tokens = auth_use_case.authenticate_user(username, password)

    return jsonify(tokens), 200


@bp.route("/api/v1/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Refreshes an access token using a valid refresh token.

    :return: A new access token.
    """
    identity = get_jwt_identity()
    claims = [("roles", get_jwt().get('roles')), ("user", get_jwt().get('user'))]
    access_token = create_access_token(identity=identity, additional_claims=claims)
    return jsonify(accessToken=access_token)


@bp.route('/api/v1/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logs out the current user by blacklisting the access token.

    :return: An empty response with status code 204.
    """
    jti = get_jwt().get('jti')
    exp = get_jwt().get('exp')
    iat = get_jwt().get('iat')

    auth_use_case.logout(jti, exp, iat)

    return jsonify(''), 204


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Checks if the access token is blacklisted.

    :param jwt_header: The JWT header.
    :param jwt_payload: The JWT payload.

    :return: True if the token is blacklisted, False otherwise.
    """
    jti = jwt_payload['jti']
    return auth_use_case.blacklist_gateway.is_token_blacklisted(jti)
