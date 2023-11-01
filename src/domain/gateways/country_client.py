from abc import ABC, abstractmethod


class ICountryClient(ABC):
    """
    An abstract base class defining the interface for fetching country data from an API.
    Implementing classes must provide a method for fetching country data.
    """

    @abstractmethod
    def fetch_data_from_api(self):
        """
        Fetch country data from an external API.

        :return: A dictionary containing country data if the request is successful, or None if there's an error.
        """
        pass
