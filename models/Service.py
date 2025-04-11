from abc import ABC, abstractmethod
from enum import Enum
from utils.logger import logger

class Service(ABC):
    class Type(Enum):
        LOAN = "loan"
        CREDIT_CARD = "credit_card"

    def __init__(self):
        self._is_active = True
        self._approved_by = None
        self._type = None 

    @property
    def type(self):
        return self._type

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = bool(value)

    def can_apply(self, customer):
        """Check if the customer can apply for this service.
        Args:
            customer (Customer): The customer to check.
        Returns:
            bool: True if the customer can apply, False otherwise.
        """
        
        if not self.is_active:
            logger.info("Service is not active.")
            return False
        
        return self._meets_requirements(customer)

    def approve(self, employee):
        """Approve the service by an employee and make it active.
        Args:
            employee (Employee): The employee approving the service.
        """
        self._approved_by = employee.full_name
        self._is_active = True
        logger.info(f"{self.type} service approved by {employee.full_name}")

    @abstractmethod
    def _meets_requirements(self, customer):
        """Check if the customer meets the requirements for this service.
        Args:
            customer (Customer): The customer to check.
        
        Returns:
            bool: True if the customer meets the requirements, False otherwise.

        Raises:
        NotImplementedError: This method must be implemented by subclasses.
        """

        raise NotImplementedError("Subclasses must implement _meets_requirements method")

    def to_dict(self):
        """Serialize the Service class to a dictionary."""
        return {
            'type': self._type, 
            'is_active': self.is_active,
            'approved_by': self._approved_by
        }