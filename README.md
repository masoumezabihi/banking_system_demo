# Banking System

A command-line banking system implementation in Python that simulates core banking operations with customer management, account handling, and banking services.

## Features

- **Customer Management**
  - Add and manage customers
  - View customer listings
  - Input validation for customer data

- **Account Operations**
  - Savings Account
  - Checking Account 
  - Deposit and withdrawal operations
  - Balance tracking

- **Banking Services**
  - Credit Card Service
  - Loan Service 
  - Service eligibility checks
  - Service status tracking

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/masoumezabihi/banking_system_demo.git
```
2. Navigate into the project directory
```bash
cd banking_system_demo
```

3. Run the program
```bash
python main.py
```

## Usage

The system presents a menu with the following options:

1. Add New Customer
2. Open Account
3. Apply for Service
4. List All Customers
5. List All Accounts
6. List All Services
7. List All Employees
8. Deposit/Withdraw
9. Exit

## Project Structure

```
banking-system/
├── main.py                 # Main program entry
├── models/                 # Core business models
├── services/              # Business logic services
├── repositories/          # Data storage handling
├── utils/                 # Utilities and constants
├── data/                 # Data storage
└── logs/                 # System logs
```

## Business Rules

### Customers
- ID: 10 digits
- Age: 18-100 years
- Phone: 10 digits

### Accounts
- Savings: Minimum $500 balance
- Checking: $500 transaction limit

### Services
- Credit Card: Minimum age 21
- Loan: Minimum age 18

## Data Storage

- Customer data stored in JSON format
- Local file-based storage system

## Logs
Log file is stored in the logs/ folder. This file contains system logs, including error messages, warnings, and other important system information.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

You can connect with me on LinkedIn: [My LinkedIn Profile](https://www.linkedin.com/in/masoume-zabihi-a7294338/)
