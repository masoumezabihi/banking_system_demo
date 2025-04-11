import json
from pathlib import Path

from utils.logger import logger
from models.Employee import Employee


class EmployeeRepository:
    def __init__(self, file_path="data/employees.json"):
        self.file_path = Path(file_path)
        self._data = []
        self._load_data()  

    def _load_data(self):
        """Load data from the JSON file, if it exists."""
        if self.file_path.exists():
            try:
                with self.file_path.open('r', encoding='utf-8') as f:
                    self._data = json.load(f)
                logger.info("Data loaded successfully.")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
        else:
            logger.warning(f"{self.file_path} does not exist.")


    def _save_data(self):
        """Save the current data to the JSON file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.file_path.open('w') as f:
                json.dump(self._data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save data to {self.file_path}: {e}")

    def add_employee(self, new_employee):
        """Add an employee to the list if the id doesn't already exist.
        Args:
            new_employee (Employee): The Employee object to add.
        """
        # Convert the Employee object to a dictionary before appending it to the list
        employee_dict = new_employee.to_dict()

        # Check if the employee already exists by id
        if any(employee['id'] == employee_dict['id'] for employee in self._data):
            logger.warning(f"Attempted to add an existing employee with ID: {employee_dict['id']}")
            return
        self._data.append(employee_dict)
        self._save_data()
        logger.info(f"Employee {new_employee.full_name} added successfully.")

    def delete_employee(self, id):
        """Delete an employee by id.
        Args:
            id (str): The id of the employee to delete.
        """
        self._data = [employee for employee in self._data if employee['id'] != id]
        if not self._data:
            logger.warning(f"Attempted to remove non-existent employee with ID: {id}")
            return
        else:
            logger.info(f"Employee with ID {id} removed successfully.")
            self._save_data()
    

    def get_all_employees(self):
        """Get the list of all employees.
        Returns:
            list: List of all employees.
        """
        return self._data

    def find_employee_by(self, id):
        """Find and return an Employee object by id.
        Args:
            id (str): The id of the employee to find.
        Returns:
            Employee: The Employee object if found, None otherwise.
        """
        data = next((employee for employee in self._data if employee['id'] == id), None)
        if not data:
            logger.warning(f"Attempted to find non-existent employee with ID: {id}")
            print(f"Employee with ID {id} not found.")
            return None
        else:
            logger.info(f"Employee with ID {id} found successfully.")
            return Employee.from_dict(data) 



