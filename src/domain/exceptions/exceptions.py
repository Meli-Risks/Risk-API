class ResourceNotFoundException(Exception):
    """
    Exception to be raised when a requested resource is not found.
    """

    def __init__(self, message):
        """
        Initialize a ResourceNotFoundException with a custom message.

        :param message: A descriptive error message.
        """
        super().__init__(message)


class OperationUnauthorizedException(Exception):
    """
    Exception to be raised when an operation is not authorized.
    """

    def __init__(self, message):
        """
        Initialize an OperationUnauthorizedException with a custom message.

        :param message: A descriptive error message.
        """
        super().__init__(message)


class InvalidCredentials(Exception):
    """
    Exception to be raised when provided credentials are invalid.
    """

    def __init__(self, message):
        """
        Initialize an InvalidCredentials exception with a custom message.

        :param message: A descriptive error message.
        """
        super().__init__(message)


class BusinessException(Exception):
    """
    General exception for business-related errors.
    """

    def __init__(self, message):
        """
        Initialize a BusinessException with a custom message.

        :param message: A descriptive error message.
        """
        super().__init__(message)


class ValidationException(Exception):
    """
    Exception to be raised when input validation fails.
    """

    def __init__(self, message, errors):
        """
        Initialize a ValidationException with a custom message and validation errors.

        :param message: A descriptive error message.
        :param errors: A dictionary or list of validation errors.
        """
        super().__init__(message)
        self.errors = errors
