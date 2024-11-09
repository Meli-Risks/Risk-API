from operator import and_

from sqlalchemy import or_

from src.application.app import db
from src.domain.gateways.treatment_gateway import IRiskTreatmentGateway
from src.infrastructure.entities.risk import Risk
from src.infrastructure.entities.treatment import RiskTreatment
from src.infrastructure.utils.query_filters import filter_entities


def apply_global_filter(query, search_string):
    """
    Apply a global filter to a SQLAlchemy query based on a search string.

    :param query: The SQLAlchemy query to which the filter is applied.
    :param search_string: The search string to filter by.

    :return: The filtered query.
    """
    if search_string is not None:
        name_search = RiskTreatment.name.ilike(f"%{search_string}%")
        description_search = RiskTreatment.description.ilike(f"%{search_string}%")
        constraints_search = RiskTreatment.constraints.ilike(f"%{search_string}%")
        risk_title_search = Risk.title.ilike(f"%{search_string}%")

        filter_criteria = or_(name_search, description_search, constraints_search, risk_title_search)

        query = query.filter(filter_criteria)
    return query


def apply_conditions(query, filters):
    """
    Apply filtering conditions to a SQLAlchemy query.

    :param query: The SQLAlchemy query to which filtering conditions are to be applied.
    :param filters: A dictionary of filtering conditions.

    :return: The filtered query.
    """
    model_mapping = {
        'RiskTreatment': RiskTreatment,
        'Risk': Risk
    }

    conditions = filter_entities(filters, model_mapping)

    if conditions:
        query = query.filter(and_(*conditions))

    return query


def apply_sorting(query, order_by, order_type):
    """
    Apply sorting to a SQLAlchemy query.

    :param query: The SQLAlchemy query to which sorting is to be applied.
    :param order_by: The attribute to order by.
    :param order_type: The order type ('asc' or 'desc').

    :return: The sorted query.
    """
    if order_type == 'asc':
        query = query.order_by(getattr(RiskTreatment, order_by))
    else:
        query = query.order_by(getattr(RiskTreatment, order_by).desc())

    return query


class RiskTreatmentRepository(IRiskTreatmentGateway):
    """
    Implementation of the IRiskTreatmentGateway interface using SQLAlchemy to manage risk treatment data.
    """

    def __init__(self):
        """
        Initialize the RiskTreatmentRepository with a connection to the database.
        """
        self.db = db

    def get_risk_treatments_by_filter(self, req):
        """
        Get a paginated list of risk treatments based on filtering criteria.

        :param req: A request object containing filtering criteria.

        :return: A paginated list of risk treatments.
        """
        query = self.db.session.query(RiskTreatment, Risk).join(Risk)
        query = apply_global_filter(query, req.global_filter)
        query = apply_conditions(query, req.filters)
        query = apply_sorting(query, req.order_by, req.order_type)

        return query.paginate(page=req.page, per_page=req.per_page, error_out=False)

    def get_risk_treatment_by_id(self, treatment_id):
        pass

    def create_risk_treatment(self, data):
        pass

    def update_risk_treatment(self, treatment, data):
        pass

    def delete_risk_treatment(self, treatment):
        pass
