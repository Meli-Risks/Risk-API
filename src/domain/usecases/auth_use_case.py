from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

from src.domain.exceptions.exceptions import InvalidCredentials
from src.domain.gateways.auth_gateway import IAuthGateway
from src.domain.gateways.blacklist_gateway import IBlackListGateway


def verify_user_has_role(roles):
    """
    Verify if the user has any roles. If not, raise an InvalidCredentials exception.

    :param roles: The user's roles.
    """
    if not roles:
        raise InvalidCredentials("Usuario inactivo")


def verify_user_state(user):
    """
    Verify the user's state. If the user is inactive, raise an InvalidCredentials exception.

    :param user: The user object.
    :return: The user if active.
    """
    if not user or user.active is False:
        raise InvalidCredentials("Usuario inactivo")
    return user


class AuthUseCase:
    """
    Use case for user authentication.
    """

    def __init__(self, auth_gateway: IAuthGateway, blacklist_gateway: IBlackListGateway):
        """
        Initialize the AuthUseCase.

        :param auth_gateway: The authentication gateway.
        :param blacklist_gateway: The blacklist gateway.
        """
        self.auth_gateway = auth_gateway
        self.blacklist_gateway = blacklist_gateway

    def authenticate_user(self, username, password):
        """
        Authenticate a user with a username and password and generate access and refresh tokens.

        :param username: The username.
        :param password: The password.

        :return: A dictionary containing the access token and refresh token.
        """
        user = self.verify_login(username, password)
        verify_user_state(user)

        roles_info = [{'name': role.name, 'identifier': role.identifier} for role in user.roles]
        roles = [role.identifier for role in user.roles]
        verify_user_has_role(roles)

        user_info = {
            'userId': user.id,
            'username': user.username,
            'email': user.email,
            'roles': roles_info
        }

        claims = [("roles", roles), ("user", user_info)]
        access_token = create_access_token(identity=user.username, additional_claims=claims)
        refresh_token = create_refresh_token(identity=user.username, additional_claims=claims)

        return {
            'accessToken': access_token,
            'refreshToken': refresh_token
        }

    def logout(self, jti, exp, iat):
        """
        Log out the user and add the token to the blacklist.

        :param jti: The JWT ID.
        :param exp: The token expiration timestamp.
        :param iat: The token issuance timestamp.
        """
        expires = exp - iat
        self.blacklist_gateway.add_token_to_blacklist(jti, expires)

    def verify_login(self, username, password):
        """
        Verify the user's login credentials.

        :param username: The username.
        :param password: The password.

        :return: The user if the credentials are valid.
        """
        user = self.auth_gateway.get_user_by_username(username)
        if not user or not check_password_hash(user.password, password):
            raise InvalidCredentials("Usuario o clave inválidos")
        return user
