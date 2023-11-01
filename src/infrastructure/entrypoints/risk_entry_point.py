from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from src.domain.models.paginated_request_dto import PaginatedRequestDto
from src.domain.usecases.risk_usecase import RiskUseCase
from src.infrastructure.decorators.role_required import role_required
from src.infrastructure.entrypoints import risk_gateway, provider_gateway, country_client, country_gateway
from src.infrastructure.utils.responses import success_data_response, success_response, success_operation_response

bp = Blueprint('risks', __name__)

risk_use_case = RiskUseCase(risk_gateway, provider_gateway, country_client, country_gateway)


@bp.route('/api/v1/risks', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST', 'VIEWER'])
def get_risks():
    """
    Retrieves a list of risks based on filtering criteria. Only role ADMIN, ANALYST and VIEWER Authorized.

    :return: A list of risk data.
    :rtype: Response
    """
    pagination_req = PaginatedRequestDto(request)
    pagination_req.add_filter('user_id', get_jwt().get('user')['userId'])
    data = risk_use_case.get_filtered_risks(pagination_req)
    return jsonify(success_data_response(data)), 200


@bp.route('/api/v1/risks', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST'])
def create_risk():
    """
    Creates a new risk.

    :return: A response indicating the successful creation of the risk. Only role ADMIN and ANALYST Authorized.
    :rtype: Response
    """
    data = request.get_json()
    user_id = get_jwt().get('user')['userId']
    new_risk = risk_use_case.create_risk(data, user_id)
    risk_id = str(new_risk['id'])
    return jsonify(success_operation_response(
        201, new_risk, "Riesgo con ID " + risk_id + " creado exitosamente")), 201


@bp.route('/api/v1/risks/<int:risk_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST'])
def update_risk(risk_id):
    """
    Updates an existing risk by ID.

    :return: A response indicating the successful update of the risk. Only role ADMIN and ANALYST Authorized.
    :rtype: Response
    """
    data = request.get_json()
    user_id = get_jwt().get('user')['userId']
    updated_risk = risk_use_case.update_risk(data, risk_id, user_id)
    return jsonify(success_operation_response(
        200, updated_risk, "Riesgo actualizado exitosamente")), 200


@bp.route('/api/v1/risks/<int:risk_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN', 'ANALYST'])
def delete_risk(risk_id):
    """
    Deletes a risk by ID.

    :return: A response indicating the successful deletion of the risk. Only role ADMIN and ANALYST Authorized.
    :rtype: Response
    """
    user_id = get_jwt().get('user')['userId']
    risk_use_case.delete_risk(risk_id, user_id)
    return jsonify(success_response(200, "Riesgo eliminado exitosamente")), 200
