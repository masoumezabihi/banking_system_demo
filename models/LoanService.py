from utils.logger import logger
from models.SavingAccount import SavingAccount
from models.Service import Service
from utils.Constants import LoanConstants

class LoanService(Service):
    def __init__(self):
        super().__init__()  
        self._type = Service.Type.LOAN.value  
        logger.info("New LoanService created.")

    def _meets_requirements(self, customer):
        """Check if the customer meets the requirements for this service.
        Args:
            customer (Customer): The customer to check.
        Returns:
            bool: True if the customer meets the requirements, False otherwise.
        """	
        has_sufficient_balance = any(
            isinstance(account, SavingAccount) and account.balance >= account.minimum_balance
            for account in customer.accounts)
        
        is_eligible_age = customer.age >= LoanConstants.MIN_AGE

        logger.debug(
        f"Loan requirement check for {customer.full_name}: "
        f"balance_ok={has_sufficient_balance}, age_ok={is_eligible_age}")
        
        return has_sufficient_balance and is_eligible_age
   
    def to_dict(self):
        """Make LoanService class JSON serializable"""
        data = super().to_dict()
        return data
    

    @classmethod
    def from_dict(cls, data):
        """Create LoanService object from a dictionary
        Args:
            data (dict): Dictionary containing service data
        Returns:
            LoanService: LoanService object
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
            logger.error(f"Invalid Loan service data: Missing key {str(e)}.")
            raise ValueError(f"Invalid Loan service data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid Loan service data: {str(e)}")
            raise ValueError(f"Invalid Loan service data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")
