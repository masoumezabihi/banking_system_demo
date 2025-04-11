
from utils.logger import logger
from models.BankAccount import BankAccount as Account
from utils.Constants import MINIMUM_BALANCE


class SavingAccount(Account):
    def __init__(self, created_by=None, balance=0):
        self._minimum_balance = MINIMUM_BALANCE  
        super().__init__(balance, created_by)
        self._type = Account.Type.SAVING.value
        logger.info(f"New SavingAccount created by {created_by}.")
       

    @property
    def minimum_balance(self):
        """Getter for minimum_balance"""
        return self._minimum_balance

    def _validate_balance(self, amount):
        """
        Ensure that the balance is not below the minimum amount required for savings accounts.

        Args:
            amount (int): New balance value to validate.

        Raises:
            ValueError: If the balance is less than the defined minimum.
        """
        if amount < self._minimum_balance:
            raise ValueError(f"Savings account balance cannot be less than ${self._minimum_balance}")

    def withdraw(self, amount):
        """
        Withdraw the specified amount if it doesn't violate the minimum balance requirement.

        Args:
            amount (int): The amount to withdraw.

        Returns:
            bool: True if the withdrawal is successful and False otherwise.
        """
        if self._balance - amount >= self._minimum_balance:
            logger.info(f"Withdrawal of ${amount} approved.")
            return super().withdraw(amount)
        else:
            logger.warning(f"Withdrawal of ${amount} denied.")
            return False
    
    def to_dict(self):
        """Make SavingAccount class JSON serializable."""
        data = super().to_dict()
        data['minimum_balance'] = self._minimum_balance
        return data

    @classmethod
    def from_dict(cls, data):
        """Create SavingAccount object from a dictionary
        Args:
            data (dict): Dictionary containing account data
            
        Returns:
            SavingAccount: SavingAccount object
            
        Raises:
            ValueError: If the data is invalid.
        """
        if not data:
            logger.error("No data provided to create saving account.")
            return None
        
        try:
            account = super().from_dict(data)
            if account:
                account._minimum_balance = data.get('minimum_balance', MINIMUM_BALANCE)
            return account
        except KeyError as e:
            logger.error(f"Invalid SavingAccount data: Missing key {str(e)}.")
            raise ValueError(f"Invalid SavingAccount data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid SavingAccount data: {str(e)}")
            raise ValueError(f"Invalid SavingAccount data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")
