from abc import ABC, abstractmethod


class ICountryGateway(ABC):
    """
    An abstract base class defining the interface for managing country-related data and flags.
    Implementing classes must provide methods for setting flags, managing country data, and deleting keys.
    """

    @abstractmethod
    def set_flag(self, flag_key, ttl=86400):
        """
        Set a flag with an optional time-to-live (TTL) in seconds.

        :param flag_key: The key to set as a flag.
        :param ttl: Optional time-to-live in seconds (default is 86400 seconds, or 24 hours).

        :return: None if the flag is successfully set.
        """
        pass

    @abstractmethod
    def check_flag(self, flag_key):
        """
        Check if a flag exists.

        :param flag_key: The key to check as a flag.

        :return: True if the flag exists, False otherwise.
        """
        pass

    @abstractmethod
    def set_countries_data(self, country_data_list):
        """
        Set country-related data as a hash.

        :param country_data_list: A list of country data objects to store.

        :return: None if the data is successfully stored.
        """
        pass

    @abstractmethod
    def get_all_countries_data(self):
        """
        Get all country-related data as a dictionary.

        :return: A dictionary of country data where the keys are country codes and values are country data objects.
        """
        pass

    @abstractmethod
    def get_countries_data_by_codes(self, country_codes):
        """
        Get country-related data for specified country codes.

        :param country_codes: A list of country codes to retrieve data for.

        :return: A dictionary of country data where the keys are country codes and values are country data objects.
        """
        pass

    @abstractmethod
    def delete(self, key):
        """
        Delete a key.

        :param key: The key to delete.

        :return: None if the key is successfully deleted.
        """
        pass
