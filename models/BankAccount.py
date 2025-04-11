from enum import Enum
from utils.logger import logger

class BankAccount:
    class Type(Enum):
        SAVING = "savings"
        CHECKING = "checking"

    def __init__(self, balance=0, created_by=None):
        self._type = None
        self._created_by = created_by
        self.balance = balance 
        logger.info(f"{self.__class__.__name__} created by: {self._created_by} with balance: ${self.balance}")


    @property
    def type(self):
        return self._type

    @property
    def balance(self):
        """Getter for balance"""
        return self._balance

    @balance.setter
    def balance(self, amount):
        """Setter for balance with basic validation
        Args:
            amount (int): New balance amount
        """
        try:
            new_amount = int(amount)
            if new_amount < 0:
                raise ValueError("Balance cannot be negative")
            self._validate_balance(new_amount)  
            self._balance = new_amount
        except ValueError:
            logger.error("Balance must be a valid number")
            raise ValueError("Balance must be a valid number")
      

    def _validate_balance(self, amount):
        """
        Hook method for balance validation.
        Subclasses should override this to enforce specific balance rules.

        Args:
            amount (int): The balance amount to validate.

        Raises:
            ValueError: If the balance does not meet subclass-specific requirements.
        """
        pass

    def withdraw(self, amount):
        """Basic withdrawal functionality
        Args:
            amount (int): Amount to withdraw
        Returns:
            bool: True if withdrawal is successful, False otherwise
        """
        self.balance -= amount
        logger.info(f"${amount} withdrawn from {self._type} account. New balance: ${self.balance}")
        return True


    def to_dict(self):
        """Make BankAccount class JSON serializable"""
        return {
            'type': self._type,
            'balance': self.balance,
            'created_by': self._created_by,
        }

    @classmethod
    def from_dict(cls, data):
        """Create BankAccount object from a dictionary
        Args:
            data (dict): Dictionary containing account data
        Returns:
            BankAccount: BankAccount object
        Raises:
            ValueError: If the data is invalid.
        """

        if not data:
            logger.error("No data provided to create BankAccount.")
            return None
        
        try:
            BankAccount = cls(balance=data.get('balance', 0), created_by=data.get('created_by'))
            BankAccount._type = data['type'] 
            logger.info(f"BankAccount createdfor user: {data.get('created_by')}") 
            return BankAccount
        except KeyError as e:
            logger.error(f"Invalid BankAccount data: Missing key {str(e)}.")
            raise ValueError(f"Invalid BankAccount data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid BankAccount data: {str(e)}")
            raise ValueError(f"Invalid BankAccount data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")
