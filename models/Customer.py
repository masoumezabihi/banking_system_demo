from utils.logger import logger
from models.BankAccount import BankAccount as Account
from models.CheckingAccount import CheckingAccount
from models.SavingAccount import SavingAccount
from utils.Constants import CustomerConstants
from .Service import Service
from .CreditCardService import CreditCardService
from .LoanService import LoanService

class Customer:
    def __init__(self, id, first_name, last_name, age, address, phone_number):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.age = age 
        self.phone_number = phone_number
        self.accounts = []
        self.services = []
        logger.info(f"New Customer created: {self.full_name}")

    @property
    def id(self):
        """Getter for id  """
        return self._id

    @id.setter
    def id(self, value):
        """Setter for id with validation
        Args:
            value (str): New id value
        
        Raises:
            ValueError: If the id is invalid.
        """
        if not value:
            logger.error("Customer ID cannot be empty")
            raise ValueError("Customer ID cannot be empty")
            
        if not value.isdigit():
            logger.error("Customer ID must contain only digits")
            raise ValueError("Customer ID must contain only digits")

        if len(value) !=  CustomerConstants.ID_LENGTH:
            logger.error(f"customer ID must be exactly {CustomerConstants.ID_LENGTH} digits")
            raise ValueError("Customer ID must be exactly 10 digits")
            
        self._id = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        """Setter for age with validation
        Args:
            value (int): New age value
        
        Raises:
            ValueError: If the age is not within the valid range.
        """
        try:
            age_value = int(value)
        except ValueError:
            logger.error("Age must be a valid number")
            raise ValueError("Age must be a valid number")

        if not CustomerConstants.MIN_AGE <= age_value <= CustomerConstants.MAX_AGE:
            logger.error(f"Age must be between {CustomerConstants.MIN_AGE} and {CustomerConstants.MAX_AGE} years")
            raise ValueError(f"Age must be between {CustomerConstants.MIN_AGE} and {CustomerConstants.MAX_AGE} years")
        
        self._age = age_value

    @property
    def full_name(self):
        """Getter for full_name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        """Setter for phone_number with validation
        Args:
            value (str): New phone number value
        
        Raises:
            ValueError: If the phone number is invalid.
        """
        if not value:
            logger.error("Phone number cannot be empty.")
            raise ValueError("Phone number cannot be empty.")

        if not value.isdigit(): 
            logger.error("Phone number must contain only digits.")
            raise ValueError("Phone number must contain only digits.")

        if len(value) != 10:
            logger.error(f"Phone number must contain exactly {CustomerConstants.PHONE_NUMBER_LENGTH} digits.")
            raise ValueError(f"Phone number must contain exactly {CustomerConstants.PHONE_NUMBER_LENGTH} digits.")

        self._phone_number = value

    @property
    def active_services(self):
        """Get a list of active services for the customer
        Returns:
            list: List of active services
        """
        return [service for service in self.services if service.is_active]

    def add_account(self, account):
        """Add an account to the customer's list of accounts
        Args:
            account (BankAccount): The account to add
        """
        logger.info(f"Account added to customer: {self.full_name}")
        self.accounts.append(account)

    def remove_account(self, account):
        """Remove an account from the customer's list of accounts
        Args:
            account (BankAccount): The account to remove
        """
        logger.info(f"Account removed from customer: {self.full_name}")
        self.accounts.remove(account)

    def can_apply_for_service(self, service):
        """Check if the customer can apply for the given service.
        Args:
            service (Service): The service to check.
        Returns:
            bool: True if the customer can apply, False otherwise.
        """
        if service.can_apply(self):
            logger.info(f"Customer {self.full_name} is eligible for {service.type} service.")
            self.services.append(service)
            return True
        else:
            logger.info(f"Customer {self.full_name} is not eligible for {service.type} service.")
            return False

    def to_dict(self):
        """Make Customer class JSON serializable"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'address': self.address,
            'phone_number': self.phone_number,
            'accounts': [account.to_dict() for account in self.accounts],
            'services': [service.to_dict() for service in self.services]
        }

    @classmethod
    def from_dict(cls, data):
        """Create Customer object from a dictionary
        Args:
            data (dict): Dictionary containing customer data
        Returns:
            Customer: Customer object
        Raises:
            ValueError: If the data is invalid.
        """
        if not data:
            logger.error("No data provided to create customer.")
            return None
        
        try:
            customer = cls(
                id=data['id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                address=data['address'],
                phone_number=data['phone_number']
            )
            
            
            for account_data in data.get('accounts', []):
                account_class = SavingAccount if account_data['type'] == Account.Type.SAVINGS.value else CheckingAccount
                account = account_class.from_dict(account_data)
                if account:
                    customer.accounts.append(account)
            
            for service_data in data.get('services', []):
                service_class = LoanService if service_data['type'] == Service.Type.LOAN.value else CreditCardService
                if service_class:
                    service = service_class.from_dict(service_data)
                    if service:
                        customer.services.append(service)
                
            return customer    
        except KeyError as e:
            logger.error(f"Invalid Customer data: Missing key {str(e)}.")
            raise ValueError(f"Invalid Customer data: Missing key {str(e)}")
    
        except ValueError as e:
            logger.error(f"Invalid Customer data: {str(e)}")
            raise ValueError(f"Invalid Customer data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")
