from flask import json

from src.domain.gateways.country_gateway import ICountryGateway
from src.infrastructure.adapters.databases import redis_db


class CountryRepository(ICountryGateway):
    """
    Implementation of the ICountryGateway interface using a Redis database to manage country-related data.
    """

    def __init__(self):
        """
        Initialize the CountryRepository with a connection to the Redis database.
        """
        self.redis = redis_db

    def set_flag(self, flag_key, ttl=86400):
        """
        Set a flag in Redis with an optional time-to-live (TTL) in seconds.

        :param flag_key: The key to set in Redis.
        :param ttl: Optional time-to-live in seconds (default is 86400 seconds, or 24 hours).
        """
        self.redis.set(flag_key, 1, ex=ttl)

    def check_flag(self, flag_key):
        """
        Check if a flag exists in Redis.

        :param flag_key: The key to check in Redis.

        :return: True if the flag exists, False otherwise.
        """
        return self.redis.exists(flag_key)

    def set_countries_data(self, country_data_list):
        """
        Set country data in Redis as a hash.

        :param country_data_list: A list of country data objects to store in Redis.
        """
        data = {}
        for country in country_data_list:
            data[country.country_code] = json.dumps(country.to_dict())
        self.redis.hmset("countries", data)

    def get_all_countries_data(self):
        """
        Get all country data stored in Redis as a dictionary.

        :return: A dictionary of country data where the keys are country codes and values are country data objects.
        """
        country_data = self.redis.hgetall("countries")
        result = {}
        for code, data in country_data.items():
            result[code.decode()] = json.loads(data)
        return result

    def get_countries_data_by_codes(self, country_codes):
        """
        Get country data for specified country codes from Redis.

        :param country_codes: A list of country codes to retrieve data for.

        :return: A dictionary of country data where the keys are country codes and values are country data objects.
        """
        country_data = self.redis.hmget("countries", country_codes)
        result = {}
        for code, data in zip(country_codes, country_data):
            if data:
                result[code] = json.loads(data)
        return result

    def delete(self, key):
        """
        Delete a key from Redis.

        :param key: The key to delete from Redis.
        """
        self.redis.delete(key)
