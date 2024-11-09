from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class RiskTreatmentSchema(Schema):
    """
    Schema for creating a new risk treatment.
    """
    name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    description = fields.String(required=True, validate=validate.Length(min=10, max=500))
    constraints = fields.String(validate=validate.Length(min=10, max=200))
    startDate = fields.DateTime(required=True, validate=validate.Regexp('^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$'))
    finalDate = fields.DateTime(required=True, validate=validate.Regexp('^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$'))
    riskId = fields.Integer(required=True)


class RiskTreatmentUpdateSchema(Schema):
    """
    Schema for updating risk treatment information.
    """
    name = fields.String(validate=validate.Length(min=3, max=100))
    description = fields.String(validate=validate.Length(min=10, max=500))
    constraints = fields.String(validate=validate.Length(min=10, max=200))
    startDate = fields.DateTime(validate=validate.Regexp('^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$'))
    finalDate = fields.DateTime(validate=validate.Regexp('^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$'))
    riskId = fields.Integer()

    @validates_schema
    def validate_fields(self, data, **kwargs):
        """
        Validate that at least one of the fields is provided for update.

        :param data: The data to validate.
        :param kwargs: Additional keyword arguments.
        """
        required_fields = ['name', 'description', 'constraints', 'startDate', 'finalDate', 'riskId']

        provided_fields = sum(1 for field in required_fields if field in data and data[field] is not None)

        if provided_fields == 0:
            raise ValidationError("Debes ingresar al menos un campo")


def build_response_dto(treatments):
    """
    Build a DTO for a list of risk treatments.

    :param treatments: A paginated list of risk treatments.

    :return: A list of DTOs for risk treatments.
    """
    data = []
    for result in treatments.items:
        treatment = result.RiskTreatment
        risk = result.Risk
        data.append({
            'id': treatment.id,
            'name': treatment.name,
            'description': treatment.description,
            'constraints': treatment.constraints,
            'startDate': treatment.start_date,
            'finalDate': treatment.final_date,
            'risk': {
                'id': risk.id,
                'title': risk.title,
                'description': risk.description,
                'impact': risk.impact,
                'probability': risk.probability,
            }
        })
    return data


def get_allowed_get_all_filters():
    """
    Get a list of allowed filters for the 'get all' operation.

    :return: A list of allowed filter definitions.
    """
    return [
        {'param': 'id', 'operator': 'equals', 'entity': 'RiskTreatment', 'field': 'id', 'type': 'number'},
        {'param': 'name', 'operator': 'contains', 'entity': 'RiskTreatment', 'field': 'name'},
        {'param': 'description', 'operator': 'contains', 'entity': 'RiskTreatment', 'field': 'description'},
        {'param': 'constraints', 'operator': 'contains', 'entity': 'RiskTreatment', 'field': 'constraints'},
        {'param': 'startDate', 'operator': 'equals', 'entity': 'RiskTreatment', 'field': 'start_date'},
        {'param': 'finalDate', 'operator': 'equals', 'entity': 'RiskTreatment', 'field': 'final_date'},
        {'param': 'risk.title', 'operator': 'equals', 'entity': 'Risk', 'field': 'id'},
    ]


def get_allowed_get_all_sort():
    """
    Get a list of allowed sorting fields for the 'get all' operation.

    :return: A list of allowed sorting fields.
    """
    return ['id', 'name', 'description', 'constraints', 'startDate', 'finalDate']
