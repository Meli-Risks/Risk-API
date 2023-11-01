from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class RiskCreateSchema(Schema):
    """
    Schema for creating a new risk.
    """
    title = fields.String(required=True, validate=validate.Length(min=3, max=100))
    description = fields.String(required=True, validate=validate.Length(min=10, max=500))
    impact = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    probability = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    countryCode = fields.String(required=True, validate=validate.Length(equal=2))
    providerId = fields.Integer(required=True)


class RiskUpdateSchema(Schema):
    """
    Schema for updating risk information.
    """
    title = fields.String(validate=validate.Length(min=3, max=100))
    description = fields.String(validate=validate.Length(min=10, max=500))
    impact = fields.Integer(validate=validate.Range(min=1, max=5))
    probability = fields.Integer(validate=validate.Range(min=1, max=5))
    countryCode = fields.String(validate=validate.Length(equal=2))
    providerId = fields.Integer()

    @validates_schema
    def validate_fields(self, data, **kwargs):
        """
        Validate that at least one of the fields is provided for update.

        :param data: The data to validate.
        :param kwargs: Additional keyword arguments.
        """
        required_fields = ['title', 'description', 'impact', 'probability', 'countryCode', 'providerId']

        provided_fields = sum(1 for field in required_fields if field in data and data[field] is not None)

        if provided_fields == 0:
            raise ValidationError("Al menos un campo debe ser ingresado")


def build_response_dto(risks, countries):
    """
    Build a DTO for a list of risks.

    :param risks: A paginated list of risks.
    :param countries: Data about countries.

    :return: A list of DTOs for risks.
    """
    results = []
    for value in risks.items:
        risk = value.Risk
        provider = value.Provider
        results.append({
            'id': risk.id,
            'title': risk.title,
            'description': risk.description,
            'impact': risk.impact,
            'probability': risk.probability,
            'country': {
                'code': risk.country_code,
                'name': countries[risk.country_code]['name'],
                'flag': countries[risk.country_code]['flag'],
            },
            'provider': {
                'id': provider.id,
                'name': provider.name
            }
        })
    return results


def build_response_basic_dto(risk):
    """
    Build a basic DTO for a risk.

    :param risk: The risk object.

    :return: A basic DTO for the risk.
    """
    return {
        'id': risk.id,
        'title': risk.title,
        'description': risk.description,
        'impact': risk.impact,
        'probability': risk.probability,
        'country': risk.country_code,
        'providerId': risk.provider_id
    }


def get_allowed_get_all_filters():
    """
    Get a list of allowed filters for the 'get all' operation.

    :return: A list of allowed filter definitions.
    """
    return [
        {'param': 'id', 'operator': 'equals', 'entity': 'Risk', 'field': 'id', 'type': 'number'},
        {'param': 'title', 'operator': 'contains', 'entity': 'Risk', 'field': 'title'},
        {'param': 'description', 'operator': 'contains', 'entity': 'Risk', 'field': 'description'},
        {'param': 'impact', 'operator': 'equals', 'entity': 'Risk', 'field': 'impact'},
        {'param': 'probability', 'operator': 'equals', 'entity': 'Risk', 'field': 'probability'},
        {'param': 'user_id', 'operator': 'equals', 'entity': 'Risk', 'field': 'user_id'},
        {'param': 'country.code', 'operator': 'equals', 'entity': 'Risk', 'field': 'country_code'},
        {'param': 'provider.id', 'operator': 'equals', 'entity': 'Provider', 'field': 'id'},
        {'param': 'provider.name', 'operator': 'contains', 'entity': 'Provider', 'field': 'name'}
    ]


def get_allowed_get_all_sort():
    """
    Get a list of allowed sorting fields for the 'get all' operation.

    :return: A list of allowed sorting fields.
    """
    return ['id', 'title', 'description', 'impact', 'probability']
