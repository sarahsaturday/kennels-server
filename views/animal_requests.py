import sqlite3
from models.animal import Animal
from models.location import Location

def get_all_animals():
    """
    Get all animals

    """
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name AS location_name,
            l.address AS location_address,
            c.name AS customer_name,
            c.email AS customer_email
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id
        """)

        animals = []
        dataset = db_cursor.fetchall()

    for row in dataset:
        # Create a Customer instance from the current row
        customer = {
            'name': row['customer_name'],
            'email': row['customer_email']
        }

        # Create an Animal instance from the current row
        animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                        row['location_id'], row['customer_id'], customer)

        # Create a Location instance from the current row
        location = {
            'name': row['location_name'],
            'address': row['location_address']
            }

        # Assign the location dictionary to the Animal's 'location' property
        animal.location = location

        # Add the dictionary representation of the animal to the list
        animals.append(animal.__dict__)

    return animals

def get_single_animal(id):
    """
    Get a single animal by ID.

    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name AS location_name,
            l.address AS location_address,
            c.name AS customer_name,
            c.email AS customer_email
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id
        WHERE a.id = ?
        """, (id, ))

        row = db_cursor.fetchone()

        if row is not None:
            # Create a Customer instance from the current row
            customer = {
                'name': row['customer_name'],
                'email': row['customer_email']
            }

            # Create an Animal instance from the current row
            animal = Animal(row['id'],
                            row['name'],
                            row['breed'],
                            row['status'],
                            row['location_id'],
                            row['customer_id'],
                            customer)

            # Create a Location instance from the current row
            location = {
                'name': row['location_name'],
                'address': row['location_address']
            }

            # Assign the location dictionary to the Animal's 'location' property
            animal.location = location

            return animal.__dict__
        else:
            return None

def create_animal(new_animal):
    """
    create animal
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
            new_animal['status'], new_animal['location_id'],
            new_animal['customer_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal

def delete_animal(id):
    """
    delete animal function
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

def update_animal(id, new_animal):
    """
    update animal
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
                new_animal['status'], new_animal['location_id'],
                new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_animals_by_location(location_id):
    """
    get animals by location

    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want,
        # including the JOIN with the Location table
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address
            c.name customer_name,
            c.email customer_email
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            # Create a Customer instance from the current row
            customer = {
                'name': row['customer_name'],
                'email': row['customer_email']
            }

            # Create an Animal instance from the current row
            animal = Animal(row['id'],
                            row['name'],
                            row['breed'],
                            row['status'],
                            row['location_id'],
                            row['customer_id'],
                            customer)

            # Create a Location instance from the current row
            location = {
                'name': row['location_name'],
                'address': row['location_address']
            }

            # Assign the location dictionary to the Animal's 'location' property
            animal.location = location

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return animals
