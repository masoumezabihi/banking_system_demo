import sys
from models.BankAccount import BankAccount as Account
from services.Bank import Bank
from models.Service import Service
from models.Employee import Employee
from utils.Constants import CustomerConstants

def get_customer_info():
    print("\n=== Enter Customer Information ===")
    print(f"(ID must be {CustomerConstants.ID_LENGTH} digits)")
    id = input("ID: ").strip()

    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    address = input("Address: ").strip()

    print(f"(Age must be between {CustomerConstants.MIN_AGE} and {CustomerConstants.MAX_AGE} years)")
    age = input("Age: ").strip()

    print(f"(Phone number must be {CustomerConstants.PHONE_NUMBER_LENGTH} digits)")
    phone_number = input("Phone Number: ").strip()

    return {
        'id': id,
        'first_name': first_name,
        'last_name': last_name,
        'age': age,
        'address': address,
        'phone_number': phone_number
    }

def get_account_data():
    print("\n=== Enter Account Information ===")
    customer_id = input("Customer ID: ").strip()

    print("\nAccount Types:\n1. Savings\n2. Checking")
    while True:
        choice = input("Select account type (1/2): ").strip()
        if choice == "1":
            account_type = Account.Type.SAVINGS.value
            break
        elif choice == "2":
            account_type = Account.Type.CHECKING.value
            break
        print("Invalid choice. Please try again.")

    initial_deposit = input("Initial Deposit Amount: $").strip()

    return {
        'customer_id': customer_id,
        'account_type': account_type,
        'initial_deposit': initial_deposit
    }

def get_service_info():
    print("\n=== Enter Service Information ===")
    customer_id = input("Customer ID: ").strip()

    print("\nService Types:\n1. Loan\n2. Credit Card")
    while True:
        choice = input("Select service type (1/2): ").strip()
        if choice == "1":
            service_type = "loan"
            break
        elif choice == "2":
            service_type = "credit-card"
            break
        print("Invalid choice. Please try again.")

    return {
        'customer_id': customer_id,
        'service_type': service_type
    }

def add_customer(bank, employee):
    try:
        info = get_customer_info()
        bank.add_customer(
            id = info['id'],
            first_name=info['first_name'],
            last_name=info['last_name'],
            age=info['age'],
            address=info['address'],
            phone_number=info['phone_number'],
            employee=employee
        )
        print("\n Customer added successfully!")
    except ValueError as e:
        print(f"\n Error adding customer: {e}")
    except Exception as e:
        print(f"\n Unexpected error: {e}")

    input("\nPress Enter to continue...")

def open_account(bank, employee):
    try:
        info = get_account_data()
        account = bank.open_account(
            customer_id=info['customer_id'],
            account_type=info['account_type'],
            initial_deposit=info['initial_deposit'],
            employee_id=employee.id
        )
        if account:
            print("\n Account opened successfully!")
        else:
            print("\n Failed to open account.")
    except Exception as e:
        print(f"\n Error: {e}")
    input("\nPress Enter to continue...")

def apply_service(bank, employee):
    try:
        info = get_service_info()
        service_type = Service.Type.LOAN.value if info['service_type'] == 'loan' else Service.Type.CREDIT_CARD.value

        can_apply = bank.apply_for_service(info['customer_id'], service_type, employee.id)

        if can_apply:
            print(f"\n Customer is eligible for {info['service_type']}")
        else:
            print(f"\n Customer is not eligible for {info['service_type']}")
    except Exception as e:
        print(f"\n Error: {e}")
    input("\nPress Enter to continue...")

def list_customers(bank):
    try:
        customers = bank.get_all_customers()
        if customers:
            print("\n=== Customer List ===")
            
            # Left-aligns the text within the specified width
            print(f"{'ID':<15}{'First Name':<15}{'Last Name':<15}{'Age':<5}{'Address':<20}{'Phone Number':<15}")
            print("-" * 80)  
            for customer in customers:
                print(f"{customer.id:<15}{customer.first_name:<15}{customer.last_name:<15}{customer.age:<5}{customer.address:<20}{customer.phone_number:<15}")
        else:
            print("\nNo customers found.")
    except Exception as e:
        print(f"\n Error listing customers: {e}")
    
    input("\nPress Enter to continue...")

def get_account_operation_data():
    print("\n=== Account Operation ===")
    customer_id = input("Customer ID: ").strip()
    
    if not customer_id:
        raise ValueError("Customer ID is required")
        
    print("\nAccount Types:\n1. Savings\n2. Checking")
    while True:
        choice = input("Select account type (1/2): ").strip()
        if choice == "1":
            account_type = Account.Type.SAVINGS.value
            break
        elif choice == "2":
            account_type = Account.Type.CHECKING.value
            break
        print("Invalid choice. Please try again.")
    
    print("\nOperation Types:\n1. Deposit\n2. Withdraw")
    while True:
        choice = input("Select operation (1/2): ").strip()
        if choice in ["1", "2"]:
            operation = "deposit" if choice == "1" else "withdraw"
            break
        print("Invalid choice. Please try again.")
    
    amount = input("Amount: $").strip()
    
    return {
        'customer_id': customer_id,
        'account_type': account_type,
        'operation': operation,
        'amount': amount
    }

def perform_account_operation(bank, employee):
    try:
        info = get_account_operation_data()
        customer = bank.find_customer(info['customer_id'])
        
        if not customer:
            print("\nCustomer not found.")
            return
            
        # Find the first account of the specified type
        account = next(
            (acc for acc in customer.accounts if acc.type == info['account_type']), 
            None
        )
        
        if not account:
            print(f"\nNo {info['account_type']} account found for this customer.")
            return
            
        amount = int(info['amount'])
        
        if info['operation'] == 'deposit':
            try:
                account.balance += amount
                print(f"\nSuccessfully deposited ${amount}. New balance: ${account.balance}")
            except ValueError as e:
                print(f"\nError during deposit: {e}")
        else:  # withdraw
            if account.withdraw(amount):
                print(f"\nSuccessfully withdrew ${amount}. New balance: ${account.balance}")
            else:
                print("\nWithdrawal failed. Insufficient funds or below minimum balance.")
                
        # Update the customer in repository
        bank.customer_repository.update_customer(customer.id, customer)
        
    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    
    input("\nPress Enter to continue...")

def list_accounts(bank):
    try:
        customers = bank.get_all_customers()
        if not customers:
            print("\nNo accounts found.")
            return

        print("\n=== Account List ===")
        print(f"{'Customer ID':<15}{'Account Type':<15}{'Balance':<15}{'Created By':<20}")
        print("-" * 65)
        
        for customer in customers:
            for account in customer.accounts:
                print(f"{customer.id:<15}{account.type:<15}${account.balance:<14}{account._created_by:<20}")
                
    except Exception as e:
        print(f"\nError listing accounts: {e}")
    
    input("\nPress Enter to continue...")

def list_services(bank):
    try:
        customers = bank.get_all_customers()
        if not customers:
            print("\nNo services found.")
            return

        print("\n=== Service List ===")
        print(f"{'Customer ID':<15}{'Customer Name':<20}{'Service Type':<15}{'Status':<10}{'Approved By':<20}")
        print("-" * 80)
        
        for customer in customers:
            for service in customer.services:
                status = "Active" if service.is_active else "Inactive"
                print(f"{customer.id:<15}{customer.first_name + ' ' + customer.last_name:<20}"
                      f"{service.type:<15}{status:<10}{service._approved_by or 'N/A':<20}")
                
    except Exception as e:
        print(f"\nError listing services: {e}")
    
    input("\nPress Enter to continue...")

def list_employees(bank):
    try:
        employees = bank.get_all_employees()
        if not employees:
            print("\nNo employees found.")
            return

        print("\n=== Employee List ===")
        print(f"{'ID':<10}{'Name':<20}{'Position':<15}")
        print("-" * 45)
        
        for employee in employees:
            print(f"{employee['id']:<10}{employee['first_name'] + ' ' + employee['last_name']:<20}"
                  f"{employee['position']:<15}")
                
    except Exception as e:
        print(f"\nError listing employees: {e}")
    
    input("\nPress Enter to continue...")

def display_menu():
    print("\n=== Banking System Menu ===")
    print("1. Add New Customer")
    print("2. Open Account")
    print("3. Apply for Service")
    print("4. List All Customers")
    print("5. List All Accounts")
    print("6. List All Services")
    print("7. List All Employees")
    print("8. Deposit/Withdraw")
    print("9. Exit")
    return input("\nSelect an option (1-9): ").strip()

def initialize_bank():
    bank = Bank()
    
    employees = bank.get_all_employees()
    if not employees:
        bank.add_employee(
            id="1",
            first_name="John",
            last_name="Smith",
            position=Employee.Position.MANAGER.value
        )
        bank.add_employee(
            id="2",
            first_name="Daniel",
            last_name="Smith",
            position=Employee.Position.TELLER.value
        )
    
    return bank

def main():
    bank = initialize_bank()
    employee = bank.find_employee("1")
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            add_customer(bank, employee)
        elif choice == "2":
            open_account(bank, employee)
        elif choice == "3":
            apply_service(bank, employee)
        elif choice == "4":
            list_customers(bank)
        elif choice == "5":
            list_accounts(bank)
        elif choice == "6":
            list_services(bank)
        elif choice == "7":
            list_employees(bank)
        elif choice == "8":
            perform_account_operation(bank, employee)
        elif choice == "9":
            print("\nThank you for using the Banking System!")
            sys.exit(0)
        else:
            print("\n Invalid option. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
