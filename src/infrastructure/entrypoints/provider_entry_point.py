from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.domain.models.paginated_request_dto import PaginatedRequestDto
from src.domain.usecases.provider_usecase import ProviderUseCase
from src.infrastructure.decorators.role_required import role_required
from src.infrastructure.entrypoints import provider_gateway, country_client, country_gateway
from src.infrastructure.utils.responses import success_data_response, success_response, success_operation_response

bp = Blueprint('providers', __name__)

provider_use_case = ProviderUseCase(provider_gateway, country_client, country_gateway)


@bp.route('/api/v1/providers', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST', 'VIEWER'])
def get_providers():
    """
    Retrieves a list of providers based on filtering criteria. Only role ADMIN, ANALYST and VIEWER Authorized.

    :return: A list of provider data.
    """
    pagination_req = PaginatedRequestDto(request)
    data = provider_use_case.get_filtered_providers(pagination_req)
    return jsonify(success_data_response(data)), 200


@bp.route('/api/v1/providers', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_provider():
    """
    Creates a new provider. Only role ADMIN Authorized.

    :return: A response indicating the successful creation of the provider.
    """
    data = request.get_json()
    new_provider = provider_use_case.create_provider(data)
    provider_id = str(new_provider['id'])
    return jsonify(success_operation_response(
        201, new_provider, "Provider created successfully with ID " + provider_id)), 201


@bp.route('/api/v1/providers/<int:provider_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN'])
def update_provider(provider_id):
    """
    Updates an existing provider by ID. Only role ADMIN Authorized.

    :return: A response indicating the successful update of the provider.
    """
    data = request.get_json()
    updated_provider = provider_use_case.update_provider(data, provider_id)
    return jsonify(success_operation_response(
        200, updated_provider, "Provider updated successfully")), 200


@bp.route('/api/v1/providers/<int:provider_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN'])
def delete_provider(provider_id):
    """
    Deletes a provider by ID. Only role ADMIN Authorized.

    :return: A response indicating the successful deletion of the provider.
    """
    provider_use_case.delete_provider(provider_id)
    return jsonify(success_response(200, "Provider deleted successfully")), 200
