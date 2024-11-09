from src.domain.gateways.blacklist_gateway import IBlackListGateway
from src.infrastructure.adapters.databases import redis_db


class BlackListRepository(IBlackListGateway):
    """
    Implementation of the IBlackListGateway interface using a Redis database to manage token blacklisting.
    """

    def __init__(self):
        """
        Initialize the BlackListRepository with a connection to the Redis database.
        """
        self.redis = redis_db

    def add_token_to_blacklist(self, jti, expires):
        """
        Add a token (by its unique identifier) to the blacklist with an optional expiration time.

        :param jti: The unique identifier of the token.
        :param expires: Optional expiration time for the token in seconds.

        :return: None if the token is successfully added to the blacklist.
        """
        self.redis.setex(jti, expires, 'Revoked')

    def is_token_blacklisted(self, jti):
        """
        Check if a token (by its unique identifier) is blacklisted.

        :param jti: The unique identifier of the token.

        :return: True if the token is blacklisted, False otherwise.
        """
        return self.redis.get(jti) is not None
