from src.domain.exceptions.exceptions import ValidationException


def validate_input(schema, data):
    """
    Validate input data against a schema and raise a ValidationException if errors are found.

    :param schema: A validation schema to check the data against.
    :param data: The data to be validated.

    :raises ValidationException: If validation errors are found, this exception is raised with error details.

    :return: None if validation is successful, or an exception is raised if validation fails.
    """
    errors = schema.validate(data)

    if errors:
        transformed_errors = [{"field": field, "errors": error_message} for field, errors in errors.items()
                              for error_message in errors]
        raise ValidationException("Error validating input data", transformed_errors)
