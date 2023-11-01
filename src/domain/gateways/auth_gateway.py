from abc import ABC, abstractmethod


class IAuthGateway(ABC):
    """
    An abstract base class defining the interface for an authentication gateway.
    Implementing classes must provide methods for user retrieval.
    """

    @abstractmethod
    def get_user_by_id(self, user_id):
        """
        Get a user by their unique identifier.

        :param user_id: The unique identifier of the user.

        :return: User object or None if the user is not found.
        """
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        """
        Get a user by their username.

        :param username: The username of the user.

        :return: User object or None if the user is not found.
        """
        pass
