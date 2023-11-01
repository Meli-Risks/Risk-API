from src.domain.exceptions.exceptions import ResourceNotFoundException, BusinessException
from src.domain.gateways.country_client import ICountryClient
from src.domain.gateways.country_gateway import ICountryGateway
from src.domain.gateways.provider_gateway import IProviderGateway
from src.domain.models.provider_dto import get_allowed_get_all_sort, ProviderCreateSchema, ProviderUpdateSchema, \
    build_response_dto, get_allowed_get_all_filters, build_response_basic_dto
from src.domain.usecases.country_use_case import CountryUseCase
from src.domain.utils.responses import response_paginated
from src.domain.utils.validations import validate_input


def get_country_codes_from_providers(providers):
    """
    Extracts unique country codes from a list of providers.

    :param providers: List of providers.

    :return: A set of unique country codes.
    """
    country_codes = []
    for provider in providers:
        country_codes.extend(provider.country_codes)

    return set(country_codes)


class ProviderUseCase:
    """
    Use case for managing provider data.
    """

    def __init__(self, provider_gateway: IProviderGateway, country_client: ICountryClient,
                 country_gateway: ICountryGateway):
        """
        Initialize the ProviderUseCase.

        :param provider_gateway: The provider data gateway.
        :param country_client: The country data client.
        :param country_gateway: The country data gateway.
        """
        self.provider_gateway = provider_gateway
        self.country_service = CountryUseCase(country_client, country_gateway)

    def get_filtered_providers(self, req):
        """
        Get a list of providers based on filtering and sorting criteria.

        :param req: PaginatedRequestDto containing filter and sorting criteria.

        :return: Paginated response with a list of filtered providers.
        """
        req.build_filter_values(get_allowed_get_all_filters())
        req.build_order_by('id', get_allowed_get_all_sort())

        providers = self.provider_gateway.get_providers_by_filter(req)
        countries_data = self.get_countries_data(providers.items)

        results = build_response_dto(providers, countries_data)
        return response_paginated(providers.total, req.page, req.per_page, providers.pages, results)

    def get_provider_by_id(self, provider_id):
        """
        Get a provider by its ID.

        :param provider_id: The ID of the provider to retrieve.

        :return: The provider with the specified ID.
        """
        return self.provider_gateway.get_provider_by_id(provider_id)

    def create_provider(self, data):
        """
        Create a new provider with the given data.

        :param data: Data for creating a new provider.

        :return: Basic information about the created provider.
        """
        validate_input(ProviderCreateSchema(), data)

        country_codes = set(data.get('countryCodes', []))
        self.validate_existence_all_country_codes(country_codes)

        new_provider = self.provider_gateway.create_provider(data)
        return build_response_basic_dto(new_provider)

    def update_provider(self, data, provider_id):
        """
        Update an existing provider with the given data.

        :param data: Data for updating the provider.
        :param provider_id: The ID of the provider to update.

        :return: Basic information about the updated provider.
        """
        validate_input(ProviderUpdateSchema(), data)

        provider_to_update = self.find_provider_by_id(provider_id)
        country_codes = set(data.get('countryCodes', provider_to_update.country_codes))
        self.validate_existence_all_country_codes(country_codes)

        update_provider = self.provider_gateway.update_provider(provider_to_update, data)
        return build_response_basic_dto(update_provider)

    def delete_provider(self, provider_id):
        """
        Delete a provider by its ID.

        :param provider_id: The ID of the provider to delete.

        :return: The ID of the deleted provider.
        """
        provider_to_delete = self.find_provider_by_id(provider_id)
        return self.provider_gateway.delete_provider(provider_to_delete)

    def find_provider_by_id(self, provider_id):
        """
        Find a provider by its ID.

        :param provider_id: The ID of the provider to find.

        :return: The provider with the specified ID.
        :raise: ResourceNotFoundException if the provider is not found.
        """
        provider = self.provider_gateway.get_provider_by_id(provider_id)

        if provider is None:
            raise ResourceNotFoundException("Proveedor no encontrado")

        return provider

    def validate_existence_all_country_codes(self, country_codes):
        """
        Validate the existence of all provided country codes.

        :param country_codes: A set of country codes to validate.

        :raise: BusinessException if some country codes do not exist.
        """
        if country_codes:
            countries_data = self.country_service.get_countries_by_codes(country_codes)
            countries = set(countries_data.keys())

            invalid_country_codes = country_codes.difference(countries)

            if invalid_country_codes:
                raise BusinessException("Algunos codigos de paises no existen")

    def get_countries_data(self, providers):
        """
        Get country data for a list of providers.

        :param providers: List of providers.

        :return: A dictionary of country data.
        """
        country_codes = get_country_codes_from_providers(providers)

        countries_data = {}
        if country_codes:
            countries_data = self.country_service.get_countries_by_codes(country_codes)

        return countries_data
