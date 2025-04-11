from utils.logger import logger
from models.BankAccount import BankAccount as Account
from utils.Constants import TRANSACTION_LIMIT 	


class CheckingAccount(Account):
    def __init__(self, balance=0, created_by=None, transaction_limit=TRANSACTION_LIMIT):
        self._type = Account.Type.CHECKING.value
        self._transaction_limit = transaction_limit  
        super().__init__(balance, created_by)
        logger.info(f"New CheckingAccount created by {created_by}.")


    @property
    def transaction_limit(self):
        return self._transaction_limit

    @transaction_limit.setter
    def transaction_limit(self, limit):
        """Setter for transaction_limit with validation
        Args:
            limit (int): New transaction limit value
        Raises:
            ValueError: If the transaction limit is invalid.
        """
        try:
            limit = int(limit)
        except ValueError:
            logger.error("Transaction limit must be a valid number.")
            raise ValueError("Transaction limit must be a valid number.")
        
        if limit > 0 and limit <= TRANSACTION_LIMIT:
            self._transaction_limit = limit
        else:
            logger.error(f"Transaction limit must be positive and less than or equal to {TRANSACTION_LIMIT}.")
            raise ValueError(f"Transaction limit must be positive and less than or equal to {TRANSACTION_LIMIT}.")

    def withdraw(self, amount):
        """Withdraw the specified amount if it doesn't violate the transaction limit.
        Args:
            amount (int): The amount to withdraw.
        Returns:
            bool: True if the withdrawal is successful and False otherwise.
        """
        if amount <= self._transaction_limit and self.balance >= amount: 
            logger.info(f"Withdrawal of ${amount} approved.")       
            return super().withdraw(amount)
        else:
            logger.warning(f"Withdrawal of ${amount} denied.")
            return False

    def to_dict(self):
        """Make CheckingAccount class JSON serializable."""
        data = super().to_dict()
        data['transaction_limit'] = self._transaction_limit
        return data

    @classmethod
    def from_dict(cls, data):
        """Create CheckingAccount object from a dictionary
        Args:
            data (dict): Dictionary containing account data
            
        Returns:
            CheckingAccount: CheckingAccount object

        Raises:
            ValueError: If the data is invalid.
        """
        if not data:
            logger.error("No data provided to create checking account.")
            return None
        
        try:
            account = super().from_dict(data)
            if account:
                account._transaction_limit = data.get('transaction_limit', TRANSACTION_LIMIT)
            return account
        except KeyError as e:
            logger.error(f"Invalid CheckingAccount data: Missing key {str(e)}.")
            raise ValueError(f"Invalid CheckingAccount data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid CheckingAccount data: {str(e)}")
            raise ValueError(f"Invalid CheckingAccount data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")