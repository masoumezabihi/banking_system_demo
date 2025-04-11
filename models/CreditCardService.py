from utils.logger import logger
from models.Service import Service
from utils.Constants import MINIMUM_BALANCE, CreditCardConstants

class CreditCardService(Service):
    def __init__(self):
        super().__init__() 
        self._type = Service.Type.CREDIT_CARD.value 
        logger.info("New CreditCardService created.")


    def _meets_requirements(self, customer):
        """Check if the customer meets the requirements for this service.
        Args:
            customer (Customer): The customer to check.
        Returns:
            bool: True if the customer meets the requirements, False otherwise.
        """
        has_sufficient_balance = any(account.balance >= MINIMUM_BALANCE for account in customer.accounts)
        is_eligible_age = customer.age >= CreditCardConstants.MIN_AGE
        logger.debug(f"CreditCard requirement check for {customer.full_name}: "
                 f"balance_ok={has_sufficient_balance}, age_ok={is_eligible_age})")
        
        return has_sufficient_balance and is_eligible_age
    

    def to_dict(self):
        """Make CreditCardService class JSON serializable"""
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data):
        """Create CreditCardService object from a dictionary
        Args:
            data (dict): Dictionary containing service data
        Returns:
            CreditCardService: CreditCardService object
        Raises:
            ValueError: If the data is invalid.
        """
        if not data:
            return None
        try:
            service = cls()
            service._is_active = data.get('is_active', True)
            service._approved_by = data.get('approved_by')
            return service
        except KeyError as e:
            logger.error(f"Invalid CreditCard service data: Missing key {str(e)}.")
            raise ValueError(f"Invalid CreditCard service data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid CreditCard service data: {str(e)}")
            raise ValueError(f"Invalid CreditCard service data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")