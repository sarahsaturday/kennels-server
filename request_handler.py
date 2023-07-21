import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import (
    get_all_animals,
    get_single_animal,
    create_animal,
    delete_animal,
    update_animal,
    get_all_locations,
    get_single_location,
    create_location,
    delete_location,
    update_location,
    get_all_employees,
    get_single_employee,
    create_employee,
    delete_employee,
    update_employee,
    get_all_customers,
    get_single_customer,
    create_customer,
    delete_customer,
    update_customer,
    get_customers_by_email
)

class HandleRequests(BaseHTTPRequestHandler):
    """
    A custom request handler class that extends the BaseHTTPRequestHandler class.

    """
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        """
        method docstring
        """
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()
            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customers_by_email(query['email'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """
        Handle HTTP POST requests.

        """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None

        # Initialize new location
        new_location = None

        # Initialize new employee
        new_employee = None

        # Initialize new customer
        new_customer = None

        # Add a new animal, location, or employee to the list
        if resource == "animals":
            new_animal = create_animal(post_body)
        elif resource == "locations":
            new_location = create_location(post_body)
        elif resource == "employees":
            new_employee = create_employee(post_body)
        elif resource == "customers":
            new_customer = create_customer(post_body)

        # Encode the new object and send in response
        if new_location is not None:
            self.wfile.write(json.dumps(new_location).encode())
        elif new_employee is not None:
            self.wfile.write(json.dumps(new_employee).encode())
        elif new_customer is not None:
            self.wfile.write(json.dumps(new_customer).encode())
        else:
            self.wfile.write(json.dumps(new_animal).encode())

    def do_PUT(self):
        """
        handle boolean value
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

            # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)
        elif resource == "customers":
            update_customer(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def _set_headers(self, status, new_location=None, new_employee=None, new_customer=None):
        """
        Set response headers.

        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        if new_location is not None:
            self.send_header('Location', f"/locations/{new_location['id']}")
        elif new_employee is not None:
            self.send_header('Location', f"/employees/{new_employee['id']}")
        elif new_customer is not None:
            self.send_header('Location', f"/customers/{new_customer['id']}")
        self.end_headers()

    def do_OPTIONS(self):
        """
        Handle HTTP OPTIONS requests.

        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        """
        Handle HTTP DELETE requests.

        """
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        if resource == "locations":
            delete_location(id)
        if resource == "employees":
            delete_employee(id)
        if resource == "customers":
            delete_customer(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """
    Start the server on port 8088 using the HandleRequests class.

    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
