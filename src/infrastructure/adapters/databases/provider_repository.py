from sqlalchemy import and_

from src.application.app import db
from src.domain.gateways.provider_gateway import IProviderGateway
from src.infrastructure.entities.provider import Provider
from src.infrastructure.utils.query_filters import filter_entities


def apply_sorting(query, order_by, order_type):
    """
    Apply sorting to a SQLAlchemy query.

    :param query: The SQLAlchemy query to which sorting is to be applied.
    :param order_by: The attribute to order by.
    :param order_type: The order type ('asc' or 'desc').

    :return: The sorted query.
    """
    if order_type == 'asc':
        query = query.order_by(getattr(Provider, order_by))
    else:
        query = query.order_by(getattr(Provider, order_by).desc())

    return query


def apply_conditions(query, filters):
    """
    Apply filtering conditions to a SQLAlchemy query.

    :param query: The SQLAlchemy query to which filtering conditions are to be applied.
    :param filters: A dictionary of filtering conditions.

    :return: The filtered query.
    """
    model_mapping = {
        'Provider': Provider
    }

    conditions = filter_entities(filters, model_mapping)

    if conditions:
        query = query.filter(and_(*conditions))

    return query


class ProviderRepository(IProviderGateway):
    """
    Implementation of the IProviderGateway interface using SQLAlchemy to manage provider data.
    """

    def __init__(self):
        """
        Initialize the ProviderRepository with a connection to the database.
        """
        self.db = db

    def get_providers_by_filter(self, req):
        """
        Get a paginated list of providers based on filtering criteria.

        :param req: A request object containing filtering criteria.

        :return: A paginated list of providers.
        """
        query = self.db.session.query(Provider)

        query = apply_conditions(query, req.filters)
        query = apply_sorting(query, req.order_by, req.order_type)

        providers = query.paginate(page=req.page, per_page=req.per_page, error_out=False)

        return providers

    def get_provider_by_id(self, provider_id):
        """
        Get a provider by their unique identifier.

        :param provider_id: The unique identifier of the provider.

        :return: Provider object or None if the provider is not found.
        """
        return Provider.query.get(provider_id)

    def create_provider(self, data):
        """
        Create a new provider with the provided data.

        :param data: A dictionary of provider data.

        :return: The created provider.
        """
        new_provider = Provider(
            name=data['name'],
            country_codes=set(data['countryCodes'])
        )

        self.db.session.add(new_provider)
        self.db.session.commit()

        return new_provider

    def update_provider(self, provider, data):
        """
        Update an existing provider with the provided data.

        :param provider: The provider to be updated.
        :param data: A dictionary of provider data to update.

        :return: The updated provider.
        """
        provider.name = data.get('name', provider.name)
        provider.country_codes = set(data.get('countryCodes', provider.country_codes))

        self.db.session.commit()

        return provider

    def delete_provider(self, provider):
        """
        Delete a provider.

        :param provider: The provider to be deleted.

        :return: The unique identifier of the deleted provider.
        """
        self.db.session.delete(provider)
        self.db.session.commit()

        return provider.id
