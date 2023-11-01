def success_response(code, message):
    """
    Generate a success response.

    :param code: The response status code.
    :param message: A success message.

    :return: A success response as a dictionary.
    """
    return {
        "code": code,
        "message": message,
    }


def success_data_response(data):
    """
    Generate a success response with data and a default success message.

    :param data: The data to include in the response.

    :return: A success response with data as a dictionary.
    """
    return success_operation_response(200, data, "Consulta exitosa")


def success_operation_response(code, data, message):
    """
    Generate a success response with data and a custom message.

    :param code: The response status code.
    :param data: The data to include in the response.
    :param message: A custom success message.

    :return: A success response with data and a custom message as a dictionary.
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }


def error_response(error_code, error_message):
    """
    Generate an error response.

    :param error_code: The error code or status code.
    :param error_message: An error message.

    :return: An error response as a dictionary.
    """
    return {
        "code": error_code,
        "message": error_message,
    }


def validations_response(errors):
    """
    Generate a response for input validation errors.

    :param errors: A list of validation errors.

    :return: A validation response as a dictionary.
    """
    return {
        "code": 400,
        "message": "Error validando campos de entrada",
        "details": errors
    }
