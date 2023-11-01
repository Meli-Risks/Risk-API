from sqlalchemy import and_, or_

from src.application.app import db
from src.domain.gateways.risk_gateway import IRiskGateway
from src.infrastructure.entities.provider import Provider
from src.infrastructure.entities.risk import Risk
from src.infrastructure.utils.query_filters import filter_entities


def apply_global_filter(query, search_string):
    """
    Apply a global filter to a SQLAlchemy query based on a search string.

    :param query: The SQLAlchemy query to which the filter is applied.
    :param search_string: The search string to filter by.

    :return: The filtered query.
    """
    if search_string is not None:
        if search_string.isdigit():
            query = query.filter(Risk.id == int(search_string))
        else:
            description_search = Risk.description.ilike(f"%{search_string}%")
            title_search = Risk.title.ilike(f"%{search_string}%")
            provider_name_search = Provider.name.ilike(f"%{search_string}%")

            filter_condition = or_(description_search, title_search, provider_name_search)

            query = query.filter(filter_condition)

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
        query = query.order_by(getattr(Risk, order_by))
    else:
        query = query.order_by(getattr(Risk, order_by).desc())

    return query


def apply_conditions(query, filters):
    """
    Apply filtering conditions to a SQLAlchemy query.

    :param query: The SQLAlchemy query to which filtering conditions are to be applied.
    :param filters: A dictionary of filtering conditions.

    :return: The filtered query.
    """
    model_mapping = {
        'Risk': Risk,
        'Provider': Provider
    }

    conditions = filter_entities(filters, model_mapping)

    if conditions:
        query = query.filter(and_(*conditions))

    return query


class RiskRepository(IRiskGateway):
    """
    Implementation of the IRiskGateway interface using SQLAlchemy to manage risk data.
    """

    def __init__(self):
        """
        Initialize the RiskRepository with a connection to the database.
        """
        self.db = db

    def get_risks_by_filter(self, req):
        """
        Get a paginated list of risks based on filtering criteria.

        :param req: A request object containing filtering criteria.

        :return: A paginated list of risks.
        """
        query = self.db.session.query(Risk, Provider).join(Provider)

        query = apply_global_filter(query, req.global_filter)
        query = apply_conditions(query, req.filters)
        query = apply_sorting(query, req.order_by, req.order_type)
        risks = query.paginate(page=req.page, per_page=req.per_page, error_out=False)

        return risks

    def get_risk_by_id(self, risk_id):
        """
        Get a risk by its unique identifier.

        :param risk_id: The unique identifier of the risk.

        :return: Risk object or None if the risk is not found.
        """
        return Risk.query.get(risk_id)

    def create_risk(self, data):
        """
        Create a new risk with the provided data.

        :param data: A dictionary of risk data.

        :return: The created risk.
        """
        new_risk = Risk(
            title=data['title'],
            description=data.get('description', None),
            impact=data.get('impact', None),
            probability=data.get('probability', None),
            user_id=data.get('userId', None),
            country_code=data['countryCode'],
            provider_id=data['providerId']
        )

        self.db.session.add(new_risk)
        self.db.session.commit()

        return new_risk

    def update_risk(self, risk, data):
        """
        Update an existing risk with the provided data.

        :param risk: The risk to be updated.
        :param data: A dictionary of risk data to update.

        :return: The updated risk.
        """
        risk.title = data.get('title', risk.title)
        risk.description = data.get('description', risk.description)
        risk.impact = data.get('impact', risk.impact)
        risk.probability = data.get('probability', risk.probability)
        risk.country_code = data.get('countryCode', risk.country_code)
        risk.provider_id = data.get('providerId', risk.provider_id)

        self.db.session.commit()

        return risk

    def delete_risk(self, risk):
        """
        Delete a risk.

        :param risk: The risk to be deleted.

        :return: The unique identifier of the deleted risk.
        """
        self.db.session.delete(risk)
        self.db.session.commit()

        return risk.id
