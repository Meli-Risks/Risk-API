from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError

from src.domain.exceptions.exceptions import ResourceNotFoundException, BusinessException, ValidationException, \
    OperationUnauthorizedException, InvalidCredentials
from src.infrastructure.utils.responses import error_response, validations_response

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('src.application.config.config')

# Initialize the SQLAlchemy database connection
db = SQLAlchemy(app)

# Initialize the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Enable CORS (Cross-Origin Resource Sharing) for the application
CORS(app, resources={
    r"/*": {
        "origins": ["https://smart-risk.tech", "http://smart-risk.tech", "http://localhost:3000"],
        "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

from src.infrastructure.entrypoints import auth_entry_point, country_entry_point
from src.infrastructure.entrypoints import risk_entry_point, provider_entry_point


@app.after_request
def add_security_headers(response):
    """
    Add security-related HTTP response headers to enhance application security.

    :param response: The Flask HTTP response.
    :return: The response with added security headers.
    """

    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = "max-age=31536000; includeSubDomains"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "DENY"
    response.headers['X-XSS-Protection'] = "1; mode=block"
    response.headers['Referrer-Policy'] = "same-origin"
    return response


@app.errorhandler(ResourceNotFoundException)
def handle_resource_not_found(error):
    """
    Handle ResourceNotFoundException and return a JSON error response with a 404 status code.

    :param error: The ResourceNotFoundException that occurred.
    :return: JSON error response indicating a resource was not found (HTTP 404).
    """
    response = error_response(404, str(error))
    return jsonify(response), 404


@app.errorhandler(BusinessException)
def handle_business_exception(error):
    """
    Handle BusinessException and return a JSON error response with a 422 status code.

    :param error: The BusinessException that occurred.
    :return: JSON error response indicating a business-related issue (HTTP 422).
    """
    response = error_response(422, str(error))
    return jsonify(response), 422


@app.errorhandler(ValidationException)
def handle_validation_exception(error):
    """
    Handle ValidationException and return a JSON error response with a 400 status code.

    :param error: The ValidationException that occurred.
    :return: JSON error response indicating validation errors (HTTP 400).
    """
    response = validations_response(error.errors)
    return jsonify(response), 400


@app.errorhandler(InvalidCredentials)
def handle_invalid_credentials(error):
    """
    Handle InvalidCredentials and return a JSON error response with a 401 status code.

    :param error: The InvalidCredentials that occurred.
    :return: JSON error response indicating invalid credentials (HTTP 401).
    """
    response = error_response(401, str(error))
    return jsonify(response), 401


@app.errorhandler(OperationUnauthorizedException)
def handle_unauthorized_operation(error):
    """
    Handle OperationUnauthorizedException and return a JSON error response with a 403 status code.

    :param error: The OperationUnauthorizedException that occurred.
    :return: JSON error response indicating unauthorized operation (HTTP 403).
    """
    response = error_response(403, str(error))
    return jsonify(response), 403


@app.errorhandler(ExpiredSignatureError)
def handle_expired_signature_error(error):
    """
    Handle ExpiredSignatureError and return a JSON error response with a 401 status code.

    :param error: The ExpiredSignatureError related to JWT.
    :return: JSON error response indicating an expired token (HTTP 401).
    """
    response = error_response(401, "Token expirado")
    print(str(error))
    return jsonify(response), 401


@app.errorhandler(DecodeError)
@app.errorhandler(InvalidTokenError)
def handle_jwt_errors(error):
    """
    Handle JWT-related errors (DecodeError and InvalidTokenError) and return a JSON error response with a 401 status code.

    :param error: The JWT-related error.
    :return: JSON error response indicating an issue with the JWT (HTTP 401).
    """
    response = error_response(401, "Token inválido")
    print(str(error))
    return jsonify(response), 401


@app.errorhandler(Exception)
def handle_unexpected_exception(e):
    """
    Handle unexpected exceptions and return a JSON error response with a 500 status code.

    :param e: The unexpected exception that occurred.
    :return: JSON error response indicating an internal server error (HTTP 500).
    """
    print(e)  # Log the unexpected error.
    response = error_response(500, "Error interno del servidor")
    return jsonify(response), 500


# Register blueprints
app.register_blueprint(risk_entry_point.bp)
app.register_blueprint(provider_entry_point.bp)
app.register_blueprint(country_entry_point.bp)
app.register_blueprint(auth_entry_point.bp)
