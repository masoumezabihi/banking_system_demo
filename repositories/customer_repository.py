import json
from pathlib import Path
from utils.logger import logger
from models.Customer import Customer

class CustomerRepository:
    def __init__(self, file_path="data/customers.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save_customers([])

    def add_customer(self, new_customer, employee):
        """Add a new customer to local storage with employee tracking.
        Args:
            new_customer (Customer): The customer object to add
            employee (Employee): The employee who created the customer
        """
        customers = self._load_customers()
        customer_dict = new_customer.to_dict()
        customer_dict['created_by'] = employee.full_name
        customers.append(customer_dict)
        self._save_customers(customers)
        logger.info(f"Customer {new_customer.full_name} added successfully.")

    def update_customer(self, customer_id, customer):
        """Update an existing customer
        Args:
            customer_id (str): The id of the customer to update
            customer (Customer): The updated customer object
        """
        customers = self._load_customers()
        for i, cust in enumerate(customers):
            if cust['id'] == customer_id:
                customer_dict = customer.to_dict()
                customers[i] = customer_dict
                self._save_customers(customers)
                logger.info(f"Customer {customer.full_name} updated successfully.")
                updated = True
                break
        if not updated:
            logger.warning(f"Attempted to update non-existent customer with ID: {customer_id}")

    def remove_customer(self, id):
        """Remove a customer by their id.
        Args:
            id (str): The id of the customer to remove
        """
        
        customers = self._load_customers()
        primary_len = len(customers)
        customers = [customer for customer in customers if customer['id'] != id]
        if primary_len == len(customers):
            logger.warning(f"Attempted to remove non-existent customer with ID: {id}")
            return 
        else:
            self._save_customers(customers)
            logger.info(f"Customer with ID {id} removed successfully.")

    def get_all_customers(self):
        """Get all customers."""
        customers = self._load_customers()
        return [Customer.from_dict(customer) for customer in customers]

    def find_customer(self, id):
        """Find a customer by their id.
        Args:
            id (str): The id of the customer to find
        """
        customers = self._load_customers()
        customer_data = next(
            (c for c in customers if c['id'] == id), 
            None
        )

        if customer_data:
          logger.info(f"Customer with ID {id} found successfully.")
          return Customer.from_dict(customer_data)
        else:
            logger.warning(f"Attempted to find non-existent customer with ID: {id}")
            return None

    def _load_customers(self):
        """Load customers from JSON file.
        returns:
            list: List of customers
        """
        if not self.file_path.exists():
            logger.error(f"Customers file({self.file_path}) not found.")
            return []
        try:
            with open(self.file_path, 'r') as f:
                logger.info(f"Customers in {self.file_path} found and loaded successfully.")
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load customers from {self.file_path}: {e}")
            return []
    

    def _save_customers(self, customers):
        """Save customers to JSON file.
        Args:
            customers (list): List of customers
        """
        try:
            with open(self.file_path, 'w') as f:
                json.dump(customers, f, indent=4)
            logger.info(f"Successfully saved customers to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save customers from {self.file_path}: {e}")
            raise
