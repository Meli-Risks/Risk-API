from abc import ABC, abstractmethod


class IRiskTreatmentGateway(ABC):
    """
    An abstract base class defining the interface for managing risk-treatment-related data.
    Implementing classes must provide methods for retrieving, creating, updating, and deleting risks.
    """

    @abstractmethod
    def get_risk_treatments_by_filter(self, req):
        """
        Get a paginated list of risk treatments based on filtering criteria.

        :param req: A request object containing filtering criteria.

        :return: A paginated list of risk treatment.
        """
        pass

    @abstractmethod
    def get_risk_treatment_by_id(self, treatment_id):
        """
        Get a risk treatment by its unique identifier.

        :param treatment_id: The unique identifier of the risk treatment.

        :return: Risk treatment object or None if the risk is not found.
        """
        pass

    @abstractmethod
    def create_risk_treatment(self, data):
        """
        Create a new risk treatment with the provided data.

        :param data: A dictionary of risk treatment data.

        :return: The created risk treatment.
        """
        pass

    @abstractmethod
    def update_risk_treatment(self, treatment, data):
        """
        Update an existing risk treatment with the provided data.

        :param treatment: The risk treatment to be updated.
        :param data: A dictionary of risk treatment data to update.

        :return: The updated risk treatment.
        """
        pass

    @abstractmethod
    def delete_risk_treatment(self, treatment):
        """
        Delete a risk treatment.

        :param treatment: The risk to be deleted.

        :return: The unique identifier of the deleted risk.
        """
        pass
