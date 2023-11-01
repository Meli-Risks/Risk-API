from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.domain.usecases.country_use_case import CountryUseCase
from src.infrastructure.decorators.role_required import role_required
from src.infrastructure.entrypoints import country_client, country_gateway
from src.infrastructure.utils.responses import success_data_response

bp = Blueprint('countries', __name__)

country_use_case = CountryUseCase(country_client, country_gateway)


@bp.route('/api/v1/countries/all', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST'])
def get_countries():
    """
    Retrieves a list of all countries. Only role ADMIN and ANALYST Authorized.

    :return: A list of country data.
    """
    api_data = country_use_case.get_all_countries()
    array = [value for value in api_data.values()]
    return jsonify(success_data_response(array)), 200


@bp.route('/api/v1/countries', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST'])
def get_countries_by_codes():
    """
    Retrieves country data by country codes. Only role ADMIN and ANALYST Authorized.

    :return: A list of country data.
    """
    country_codes = request.args.getlist('codes')

    if not country_codes:
        return jsonify({"message": "No se proporcionaron códigos de países"})

    api_data = country_use_case.get_countries_by_codes(country_codes)

    array = [value for value in api_data.values()]
    return jsonify(success_data_response(array)), 200
