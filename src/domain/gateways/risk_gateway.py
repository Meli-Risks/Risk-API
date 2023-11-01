from abc import abstractmethod, ABC


class IRiskGateway(ABC):
    """
    An abstract base class defining the interface for managing risk-related data.
    Implementing classes must provide methods for retrieving, creating, updating, and deleting risks.
    """

    @abstractmethod
    def get_risks_by_filter(self, req):
        """
        Get a paginated list of risks based on filtering criteria.

        :param req: A request object containing filtering criteria.

        :return: A paginated list of risks.
        """
        pass

    @abstractmethod
    def get_risk_by_id(self, risk_id):
        """
        Get a risk by its unique identifier.

        :param risk_id: The unique identifier of the risk.

        :return: Risk object or None if the risk is not found.
        """
        pass

    @abstractmethod
    def create_risk(self, data):
        """
        Create a new risk with the provided data.

        :param data: A dictionary of risk data.

        :return: The created risk.
        """
        pass

    @abstractmethod
    def update_risk(self, risk, data):
        """
        Update an existing risk with the provided data.

        :param risk: The risk to be updated.
        :param data: A dictionary of risk data to update.

        :return: The updated risk.
        """
        pass

    @abstractmethod
    def delete_risk(self, risk):
        """
        Delete a risk.

        :param risk: The risk to be deleted.

        :return: The unique identifier of the deleted risk.
        """
        pass
