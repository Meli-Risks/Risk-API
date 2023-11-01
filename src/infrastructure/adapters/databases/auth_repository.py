from src.domain.gateways.auth_gateway import IAuthGateway
from src.infrastructure.entities.user import User


class AuthRepository(IAuthGateway):
    """
    Implementation of the IAuthGateway interface using a User entity.
    This repository provides methods for user retrieval.
    """

    def get_user_by_id(self, user_id):
        """
        Get a user by their unique identifier.

        :param user_id: The unique identifier of the user.

        :return: User object or None if the user is not found.
        """
        return User.query.get(user_id)

    def get_user_by_username(self, username):
        """
        Get a user by their username.

        :param username: The username of the user.

        :return: User object or None if the user is not found.
        """
        return User.query.filter_by(username=username).first()
