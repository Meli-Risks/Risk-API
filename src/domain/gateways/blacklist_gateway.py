from abc import ABC, abstractmethod


class IBlackListGateway(ABC):
    """
    An abstract base class defining the interface for a token blacklist gateway.
    Implementing classes must provide methods to add tokens to the blacklist and check if a token is blacklisted.
    """

    @abstractmethod
    def add_token_to_blacklist(self, jti, expires):
        """
        Add a token (by its unique identifier) to the blacklist with an optional expiration time.

        :param jti: The unique identifier of the token.
        :param expires: Optional expiration time for the token in seconds.

        :return: None if the token is successfully added to the blacklist.
        """
        pass

    @abstractmethod
    def is_token_blacklisted(self, jti):
        """
        Check if a token (by its unique identifier) is blacklisted.

        :param jti: The unique identifier of the token.

        :return: True if the token is blacklisted, False otherwise.
        """
        pass
