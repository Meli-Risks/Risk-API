import requests

from src.domain.gateways.country_client import ICountryClient


class CountryClient(ICountryClient):
    """
    Implementation of the ICountryClient interface to fetch country data from a REST API.
    """

    def __init__(self):
        """
        Initialize the CountryClient with the API URL for fetching country data.
        """
        self.api_url = 'https://restcountries.com/v3.1/all'

    def fetch_data_from_api(self):
        """
        Fetch country data from the configured API.

        :return: A dictionary containing country data if the request is successful, or None if there's an error.
        """
        response = requests.get(self.api_url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
