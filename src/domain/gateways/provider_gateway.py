from abc import ABC, abstractmethod


class IProviderGateway(ABC):
    """
    An abstract base class defining the interface for managing provider data.
    Implementing classes must provide methods for retrieving, creating, updating, and deleting providers.
    """

    @abstractmethod
    def get_providers_by_filter(self, req):
        """
        Get a paginated list of providers based on filtering criteria.

        :param req: A request object containing filtering criteria.

        :return: A paginated list of providers.
        """
        pass

    @abstractmethod
    def get_provider_by_id(self, provider_id):
        """
        Get a provider by their unique identifier.

        :param provider_id: The unique identifier of the provider.

        :return: Provider object or None if the provider is not found.
        """
        pass

    @abstractmethod
    def create_provider(self, data):
        """
        Create a new provider with the provided data.

        :param data: A dictionary of provider data.

        :return: The created provider.
        """
        pass

    @abstractmethod
    def update_provider(self, provider, data):
        """
        Update an existing provider with the provided data.

        :param provider: The provider to be updated.
        :param data: A dictionary of provider data to update.

        :return: The updated provider.
        """
        pass

    @abstractmethod
    def delete_provider(self, provider):
        """
        Delete a provider.

        :param provider: The provider to be deleted.

        :return: The unique identifier of the deleted provider.
        """
        pass
