from enum import Enum

from utils.logger import logger

class Employee:
    
    class Position(Enum):
        MANAGER = "Manager"
        TELLER = "Teller"
        SENIOR_TELLER = "Senior Teller"
        LOAN_OFFICER = "Loan Officer"

    def __init__(self, id, first_name, last_name, position):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        logger.info(f"New Employee created: {self.full_name}")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def can_approve_loans(self):
        """Check if employee can approve loans
         Returns:
            bool: True if employee can approve loans, False otherwise
        """
        approveLoan = self.position.value in {self.Position.MANAGER.value, self.Position.LOAN_OFFICER.value}
        if (approveLoan):
            logger.info(f"{self.full_name} can approve loans.")
        else:
            logger.info(f"{self.full_name} cannot approve loans.")
        return approveLoan
    
    def can_open_accounts(self):
        """Check if employee can open new accounts
         Returns:
            bool: True if employee can open accounts, False otherwise
        """
        canOpen = self.position.value in {self.Position.MANAGER.value, self.Position.TELLER.value, self.Position.SENIOR_TELLER.value}
        if (canOpen):
            logger.info(f"{self.full_name} can open accounts.")
        else:
            logger.info(f"{self.full_name} cannot open accounts.")
        return canOpen

    def to_dict(self):
        """Make Employee class JSON serializable"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position
        }

    @classmethod
    def from_dict(cls, data):
        """Create Employee object from a dictionary
        Args:
            data (dict): Dictionary containing employee data
        Returns:
            Employee: Employee object
        Raises:
            ValueError: If the data is invalid.
        """
        if not data:
            logger.error("No data provided to create employee.")
            return None
        
        try:
            return cls(
                id=data['id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                position=cls.Position(data['position'])   )
        except KeyError as e:
            logger.error(f"Invalid Employee data: Missing key {str(e)}.")
            raise ValueError(f"Invalid Employee data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid Employee data: {str(e)}")
            raise ValueError(f"Invalid Employee data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")
