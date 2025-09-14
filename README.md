



# Subscription Management System

  

A comprehensive Python application for managing subscriptions, members, plans, and payments.

  

## Features

  

- **Member Management**: Add, view, edit, and manage member information

- **Plan Management**: Create and manage subscription plans with pricing and duration

- **Subscription Management**: Handle member subscriptions to plans

- **Payment Management**: Record and track payments for subscriptions

- **Reporting**: Generate various reports for business insights

- **Database**: SQLite database for data persistence

  

## Project Structure

  

```

SubscriptionManagementSystem/

├── subscription_manager/          # Main package

│   ├── __init__.py               # Package initialization

│   ├── main.py                   # Main application entry point

│   ├── models.py                 # Data models

│   ├── database.py               # Database operations

│   ├── core/                     # Business logic

│   │   ├── __init__.py

│   │   ├── members.py            # Member management

│   │   ├── plans.py              # Plan management

│   │   ├── subscriptions.py      # Subscription management

│   │   └── payments.py           # Payment management

│   ├── utils/                    # Utility functions

│   │   ├── __init__.py

│   │   ├── display.py            # Display functions

│   │   ├── helpers.py            # Helper functions

│   │   └── validators.py         # Validation functions

│   └── tests/                    # Test files

│       ├── __init__.py

│       ├── test_members.py

│       ├── test_plans.py

│       └── test_subscriptions.py

├── data/                         # Database storage

├── requirements.txt              # Python dependencies

├── .gitignore                    # Git ignore rules

└── README.md                     # This file

```

  

## Requirements

  

- Python 3.7 or higher

- No external dependencies (uses only Python standard library)

  

## Installation

  

1. Clone the repository:

```bash

git clone <[your-repo-url](https://github.com/George1712/subscription-management-system)>

cd SubscriptionManagementSystem

```

  

2. The project uses only Python standard library, so no additional installation is required.

  

## Usage

  

### Running the Application

  

Run the main application:

```bash

python subscription_manager/main.py

```

  

### Available Operations

  

1. **Member Management**
  
   - Add new members
   - View member details
   - Edit member information
   - Search members
   - Update member status

  

2. **Plan Management**

   - Create subscription plans
   - View plan details
   - Edit plans
   - Manage plan status

  

3. **Subscription Management**

   - Create subscriptions
   - View subscription details
   - Manage subscription status

  

4. **Payment Management**

   - Record payments
   - View payment history
   - Generate payment reports

  

5. **Reports**

   - System summary
   - Active members
   - Expiring subscriptions
   - Revenue reports
   - Plan popularity

  

## Database

  

The application uses SQLite database (`data/subscription_manager.db`) for data persistence. The database is automatically created and initialized when the application starts.

  

## Development

  

### Code Structure

  

- **Clean Architecture**: Separation of concerns with core business logic, utilities, and models

- **Package Structure**: Proper Python package organization with `__init__.py` files

- **Type Hints**: Uses Python typing for better code documentation

- **Error Handling**: Comprehensive error handling and user feedback

  
  

## Contributing


1. Fork the repository

2. Create a feature branch

3. Make your changes

4. Test your changes

5. Submit a pull request

  

## License

  

This project is open source and available under the MIT License.
