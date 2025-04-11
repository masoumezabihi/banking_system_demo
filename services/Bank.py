
from models.CheckingAccount import CheckingAccount
from models.SavingAccount import SavingAccount
from models.CreditCardService import CreditCardService
from models.LoanService import LoanService
from models.Service import Service
from models.BankAccount import BankAccount as Account
from models.Employee import Employee
from repositories.customer_repository import CustomerRepository
from repositories.employee_repository import EmployeeRepository
from models.Customer import Customer

class Bank:
    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.employee_repository = EmployeeRepository()

    def add_employee(self, id, first_name, last_name, position):
        """Add a new employee to the bank
        Args:
            id (str): The employee's id
            first_name (str): The employee's first name
            last_name (str): The employee's last name
            position (str): The employee's position
        	"""
        employee = Employee(
            id=id,
            first_name=first_name,
            last_name=last_name,
            position=position
        )
        self.employee_repository.add_employee(employee)
        return employee

    def find_employee(self, id):
        """Find an employee by their id
        Args:
            id (str): The id of the employee to find
        	Returns:
            Employee: The employee object if found, None otherwise
        """
        return self.employee_repository.find_employee_by(id)

    def get_all_employees(self):
        """Get all employees
        Returns:
            list: List of all employees
        """
        return self.employee_repository.get_all_employees()

    def apply_for_service(self, customer_id, service_type, employee_id):
        """Apply for a service for a customer
        Args:
            customer_id (str): The customer's id
            service_type (str): The type of service to apply for
            employee_id (str): The id of the employee applying for the service
        """
        employee = self.find_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        
        if service_type == Service.Type.LOAN.value:
            if not employee.can_approve_loans():
                  raise ValueError("Employee is not authorized to apply for service")
            service = LoanService()
        elif service_type == Service.Type.CREDIT_CARD.value:
            service = CreditCardService()
        else:
            return False
        
        customer = self.find_customer(customer_id)
        if not customer:
            return False

        canApply = customer.can_apply_for_service(service)
        if canApply:
            service.approve(self.find_employee(employee_id))
        customer.services.append(service)
        self.customer_repository.update_customer(customer.id, customer)
        return canApply

    def open_account(self, customer_id, account_type, initial_deposit, employee_id):
        """Open a new account for a customer
        Args:
            customer_id (str): The customer's id
            account_type (str): The type of account to open
            initial_deposit (float): The initial deposit amount
            employee_id (str): The id of the employee opening the account
        """
        employee = self.find_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
            
        if not employee.can_open_accounts():
            raise ValueError("Employee is not authorized to open accounts")

        customer = self.find_customer(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        if account_type == Account.Type.SAVINGS.value:
            account = SavingAccount(created_by=employee.full_name, balance=initial_deposit)
        elif account_type == Account.Type.CHECKING.value:
            account = CheckingAccount(created_by=employee.full_name, balance=initial_deposit)
        else:
            raise ValueError("Invalid account type")

        customer.add_account(account)
        self.customer_repository.update_customer(customer.id, customer)
        return account

    def add_customer(self, id, first_name, last_name, age, address, phone_number, employee):
        """Add a new customer to the bank
        Args:
            id (str): The customer's id
            first_name (str): The customer's first name
            last_name (str): The customer's last name
            age (int): The customer's age
            address (str): The customer's address
            phone_number (str): The customer's phone number
        """
        customer = Customer(
            id=id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            address=address,
            phone_number=phone_number
        )
        self.customer_repository.add_customer(customer,employee)
        return customer

    def remove_customer(self, id):
        """Remove a customer by their id
        Args:
            id (str): The id of the customer to remove
        """
        return self.customer_repository.remove_customer(id)

    def get_all_customers(self):
        """Get all customers
        Returns:
            list: List of all customers
        """
        return self.customer_repository.get_all_customers()

    def find_customer(self, id):
        """Find a customer by their id
        Args:
            id (str): The id of the customer to find
        """
        return self.customer_repository.find_customer(id)



