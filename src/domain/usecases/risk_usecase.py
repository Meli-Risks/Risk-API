from src.domain.exceptions.exceptions import ResourceNotFoundException, BusinessException, \
    OperationUnauthorizedException
from src.domain.gateways.country_client import ICountryClient
from src.domain.gateways.country_gateway import ICountryGateway
from src.domain.gateways.provider_gateway import IProviderGateway
from src.domain.gateways.risk_gateway import IRiskGateway
from src.domain.models.risk_dto import get_allowed_get_all_filters, RiskUpdateSchema, RiskCreateSchema, \
    build_response_dto, \
    get_allowed_get_all_sort, build_response_basic_dto
from src.domain.usecases.country_use_case import CountryUseCase
from src.domain.usecases.provider_usecase import ProviderUseCase
from src.domain.utils.responses import response_paginated
from src.domain.utils.validations import validate_input


def validate_risk_belongs_to_user(risk, user_id):
    """
    Validate if a given risk belongs to a specific user.

    :param risk: The risk object to be checked.
    :param user_id: The user identifier to compare with the risk's user_id.

    :raises OperationUnauthorizedException: If the user is not authorized to perform the operation.

    :return: None
    """

    if risk.user_id != user_id:
        raise OperationUnauthorizedException("No autorizado para realizar operación")


def validate_provider_has_country(provider, country_code):
    """
    Validate if a provider has a specific country within its list of associated countries.

    :param provider: The provider object to be checked.
    :param country_code: The country code to be verified within the provider's country codes.

    :raises BusinessException: If the specified country is not associated with the provider.

    :return: None
    """

    if country_code not in provider.country_codes:
        raise BusinessException("Pais no encontrado para este proveedor")


def get_country_codes_from_risks(risks):
    """
    Extract unique country codes from a list of risk objects.

    :param risks: A list of risk objects from which country codes will be extracted.

    :return: A set containing unique country codes found within the list of risks.
    """

    country_codes = set()  # Initialize an empty set to store unique country codes
    for value in risks:
        country_codes.add(value.Risk.country_code)

    return country_codes


class RiskUseCase:
    """
    Use case for managing risk data.
    """

    def __init__(self, risk_gateway: IRiskGateway, provider_gateway: IProviderGateway,
                 country_client: ICountryClient, country_gateway: ICountryGateway):
        """
        Initializes a RiskUseCase instance.

        :param risk_gateway: The risk gateway providing access to risk data.
        :param provider_gateway: The provider gateway providing access to provider data.
        :param country_client: The country client for fetching country data.
        :param country_gateway: The country gateway providing access to country data.
        """
        self.risk_gateway = risk_gateway
        self.provider_service = ProviderUseCase(provider_gateway, country_client, country_gateway)
        self.country_service = CountryUseCase(country_client, country_gateway)

    def get_filtered_risks(self, req):
        """
        Retrieves and filters a list of risks based on the provided request.

        :param req: The request containing filter criteria, pagination, and sorting details.

        :return: A paginated list of risk data based on the provided request.
        """
        req.build_filter_values(get_allowed_get_all_filters())
        req.build_order_by('id', get_allowed_get_all_sort())

        risks = self.risk_gateway.get_risks_by_filter(req)

        countries = self.get_countries_data(risks.items)
        results = build_response_dto(risks, countries)

        return response_paginated(risks.total, req.page, req.per_page, risks.pages, results)

    def create_risk(self, data, user_id):
        """
        Creates a new risk entry based on the provided data.

        :param data: The data to create the new risk.
        :param user_id: The user identifier creating the risk.

        :return: Basic information about the newly created risk.
        """
        validate_input(RiskCreateSchema(), data)

        provider_id = data.get('providerId')
        provider = self.provider_service.find_provider_by_id(provider_id)

        country_code = data.get('countryCode')
        validate_provider_has_country(provider, country_code)

        data['userId'] = user_id
        new_risk = self.risk_gateway.create_risk(data)

        return build_response_basic_dto(new_risk)

    def update_risk(self, data, risk_id, user_id):
        """
        Updates an existing risk based on the provided data.

        :param data: The data to update the risk.
        :param risk_id: The identifier of the risk to update.
        :param user_id: The user identifier updating the risk.

        :return: Basic information about the updated risk.
        """
        validate_input(RiskUpdateSchema(), data)

        risk_to_update = self.find_risk_by_id(risk_id)
        validate_risk_belongs_to_user(risk_to_update, user_id)

        provider_id = data.get('providerId', risk_to_update.provider_id)
        provider = self.provider_service.find_provider_by_id(provider_id)

        country_code = data.get('countryCode', risk_to_update.country_code)
        validate_provider_has_country(provider, country_code)

        updated_risk = self.risk_gateway.update_risk(risk_to_update, data)

        return build_response_basic_dto(updated_risk)

    def delete_risk(self, risk_id, user_id):
        """
        Deletes a risk based on the provided risk identifier and user identifier.

        :param risk_id: The identifier of the risk to delete.
        :param user_id: The user identifier deleting the risk.

        :return: A message indicating the result of the delete operation.
        """
        risk_to_delete = self.find_risk_by_id(risk_id)
        validate_risk_belongs_to_user(risk_to_delete, user_id)

        return self.risk_gateway.delete_risk(risk_to_delete)

    def find_risk_by_id(self, risk_id):
        """
        Finds a risk by its identifier.

        :param risk_id: The identifier of the risk to find.

        :raises ResourceNotFoundException: If the risk is not found.

        :return: The risk object if found.
        """
        risk = self.risk_gateway.get_risk_by_id(risk_id)

        if risk is None:
            raise ResourceNotFoundException("Riesgo no encontrado")

        return risk

    def get_countries_data(self, risks):
        """
        Retrieves country data for a list of risks.

        :param risks: A list of risk objects for which country data is needed.

        :return: A dictionary containing country data for the list of risks.
        """
        country_codes = get_country_codes_from_risks(risks)

        countries = {}
        if country_codes:
            countries = self.country_service.get_countries_by_codes(country_codes)

        return countries
