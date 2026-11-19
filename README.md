# Restaurant Relational Database

A Python and MySQL project designed to model and manage the database operations of a proposed restaurant.

## Project Overview

This project explores the design and implementation of a relational database for a restaurant environment. It combines MySQL database management with Python GUI components to retrieve and display information stored in the database.

The project demonstrates how a relational database can organize restaurant information and how Python can interact with a MySQL database to present that information through a graphical interface.

## Technologies Used

- **Python** – Application logic and database interaction
- **MySQL** – Relational database management system
- **MySQL Connector/Python** – Connecting Python applications to MySQL
- **FreeSimpleGUI** – Graphical user interface development

## Features

- MySQL database connectivity
- Employee information retrieval
- Graphical employee table viewer
- Dynamic table display using database query results
- Ability to refresh displayed information from the database

## Repository Structure

```text
Restaurant-Relational-Database/
│
├── GUI/
│   └── GUI application files
│
├── SQL/
│   └── Database scripts
│
├── EmployeeTableReader.py
├── GUI_Test.py
└── README.md
```

## Getting Started

### Prerequisites

- Python installed
- MySQL Server installed and running
- MySQL database configured with the required tables

### Installation

1. Clone the repository:

```bash
git clone https://github.com/MLucas41/Restaurant-Relational-Database.git
```

2. Navigate to the project directory:

```bash
cd Restaurant-Relational-Database
```

3. Install the required Python packages:

```bash
pip install mysql-connector-python FreeSimpleGUI
```

### Database Configuration

1. Open MySQL Workbench or another MySQL client.
2. Execute the appropriate SQL scripts located in the `SQL/` directory to configure the database.
3. Ensure the database is named `lukes_lasagna`.
4. Configure your database connection credentials using environment variables.

The Python application expects a local MySQL server and an `employees` table.

### Running the Application

To launch the employee table viewer:

```bash
python EmployeeTableReader.py
```

The application retrieves employee records from MySQL and displays them in a graphical table. The Refresh button retrieves the latest records from the database.

## Project Goals and Learning Outcomes

This project provided practical experience with:

- Relational database design and implementation
- SQL and MySQL database management
- Connecting Python applications to external databases
- Retrieving and displaying database records
- Building graphical interfaces with Python

**Author:** Luke Mertlich

**Project Type:** Academic / Personal Project
