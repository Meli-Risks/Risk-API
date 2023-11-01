from src.domain.gateways.country_client import ICountryClient
from src.domain.gateways.country_gateway import ICountryGateway
from src.domain.models.country_dto import build_country_dto


def transform_data(country_data):
    """
    Transform raw country data into a list of CountryDTO objects.

    :param country_data: List of raw country data.

    :return: List of CountryDTO objects.
    """
    country_dto_list = []
    for country in country_data:
        country_dto = build_country_dto(country)
        country_dto_list.append(country_dto)
    return country_dto_list


class CountryUseCase:
    """
    Use case for managing country data.
    """

    def __init__(self, country_client: ICountryClient, country_gateway: ICountryGateway):
        """
        Initialize the CountryUseCase.

        :param country_client: The country data client.
        :param country_gateway: The country data gateway.
        """
        self.country_client = country_client
        self.country_gateway = country_gateway

    def get_all_countries(self):
        """
        Get all countries from the cache. If not available, fetch and store data from the client.

        :return: A dictionary of country data.
        """
        self.verify_countries_in_redis()
        countries = self.country_gateway.get_all_countries_data()
        return countries

    def get_countries_by_codes(self, country_codes):
        """
        Get country data for a list of country codes from the cache. If not available, fetch and store data from the client.

        :param country_codes: List of country codes to fetch.

        :return: A dictionary of country data for the specified country codes.
        """
        self.verify_countries_in_redis()
        country_data = self.country_gateway.get_countries_data_by_codes(country_codes)
        return country_data

    def verify_countries_in_redis(self):
        """
        Verify if country data is available in the cache. If not, fetch data from the client and store it in the gateway.
        """
        if not self.country_gateway.check_flag("exist_country_data"):
            self.country_gateway.delete("countries")
            countries = transform_data(self.country_client.fetch_data_from_api())
            self.country_gateway.set_countries_data(countries)
            self.country_gateway.set_flag("exist_country_data")
