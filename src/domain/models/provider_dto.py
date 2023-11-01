from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ProviderCreateSchema(Schema):
    """
    Schema for creating a new provider.
    """
    name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    countryCodes = fields.List(fields.String(), validate=validate.Length(min=1))


class ProviderUpdateSchema(Schema):
    """
    Schema for updating a provider's information.
    """
    name = fields.String(validate=validate.Length(min=3, max=100))
    countryCodes = fields.List(fields.String(), validate=validate.Length(min=1))

    @validates_schema
    def validate_fields(self, data, **kwargs):
        """
        Validate that at least one of the fields is provided for update.

        :param data: The data to validate.
        :param kwargs: Additional keyword arguments.
        """
        required_fields = ['name', 'countryCodes']

        provided_fields = sum(1 for field in required_fields if field in data and data[field] is not None)

        if provided_fields == 0:
            raise ValidationError("Al menos un campo debe ser ingresado")


def build_response_dto(providers, countries_data):
    """
    Build a DTO for a list of providers.

    :param providers: A paginated list of providers.
    :param countries_data: Data about countries.

    :return: A list of DTOs for providers.
    """
    results = []
    for provider in providers.items:
        countries = build_response_countries(provider.country_codes, countries_data)
        results.append({
            'id': provider.id,
            'name': provider.name,
            'countries': countries
        })
    return results


def build_response_basic_dto(provider):
    """
    Build a basic DTO for a provider.

    :param provider: The provider object.

    :return: A basic DTO for the provider.
    """
    return {
        'id': provider.id,
        'name': provider.name,
        'countries': provider.country_codes
    }


def build_response_countries(country_codes, countries_data):
    """
    Build a DTO for a list of countries.

    :param country_codes: List of country codes.
    :param countries_data: Data about countries.

    :return: A list of DTOs for countries.
    """
    countries = []
    for country in country_codes:
        countries.append({
            'code': country,
            'name': countries_data[country]['name'],
            'flag': countries_data[country]['flag'],
        })
    return countries


def get_allowed_get_all_filters():
    """
    Get a list of allowed filters for the 'get all' operation.

    :return: A list of allowed filter definitions.
    """
    return [
        {'param': 'id', 'operator': 'equals', 'entity': 'Provider', 'field': 'id', 'type': 'number'},
        {'param': 'name', 'operator': 'contains', 'entity': 'Provider', 'field': 'name'}
    ]


def get_allowed_get_all_sort():
    """
    Get a list of allowed sorting fields for the 'get all' operation.

    :return: A list of allowed sorting fields.
    """
    return ['id', 'name']
