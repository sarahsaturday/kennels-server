class Animal():
    """
    new Animal class
    """
    def __init__(self, id, name, breed, status, location_id, customer_id, customer=None):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id
        self.location = None
        self.customer = customer