# bbmgt - Basketball League Management System

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Usage](#usage)
   - [Restoring the Database](#restoring-the-database)

## Introduction

**bbmgt** is a basketball league management system created to efficiently monitor game statistics and rankings for a recent basketball tournament. It offers an intuitive interface for tracking game results, player performances, and league standings.

## Getting Started

To begin using **bbmgt**, follow the steps below:

### Prerequisites

Before you get started, ensure that the following software is installed on your system:

- Python 3.7+
- Django 3.0+

### Installation

1. Clone the repository to your local machine:
2. Navigate to the project directory:
   cd bbmgt
3. Create a virtual environment:
   python -m venv venv
4. Activate the virtual environment:
   source venv/bin/activate

### Usage

To run bbmgt locally, use the following command:
   python manage.py runserver

### Restoring the Database

To restore the database using the provided backup.json file, follow these steps:

    Ensure that your bbmgt Django project is properly set up and running.

    Open a terminal and navigate to the project directory.

    Run the following command to load data from the backup.json file into your database:   
        python manage.py loaddata backup.json
    This command will populate your database with data from the backup file.

Confirm that the data has been successfully restored by accessing your bbmgt application.
