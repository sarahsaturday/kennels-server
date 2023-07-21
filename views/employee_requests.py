import sqlite3
from models import Employee

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]

def get_all_employees():
    """
    Get all employees

    """
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l ON l.id = e.location_id
        """)

        employees = []
        dataset = db_cursor.fetchall()

    for row in dataset:
        # Create a Location instance from the current row
        location = {
            'name': row['location_name'],
            'address': row['location_address']
            }

        # Create an Employee instance from the current row
        employee = Employee(
            row['id'],
            row['name'],
            location  # Pass the location dictionary to the Employee's 'location' property
            )

        employees.append(employee.__dict__)

    return employees

def get_single_employee(id):
    """
    Get a single employee by ID.

    """
    requested_employee = None

    for employee in EMPLOYEES:
        if employee["id"] == id:
            requested_employee = employee
    return requested_employee

def create_employee(employee):
    """
    Create a new employee and add it to the list of employees.

    Args:
        employee (dict): A dictionary representing the new employee to be created.

    Returns:
        dict: The dictionary representing the new employee with the 'id' property added.

    """
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

def delete_employee(id):
    """
    delete employee

    """
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    """
    update employee
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Employee
            SET
                name = ?,
        WHERE id = ?
        """, (new_employee['name'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
    