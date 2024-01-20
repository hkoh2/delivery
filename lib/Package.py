# Package.py

class Package:
    # Initialize package
    def __init__(self,
                 package_id,
                 address,
                 city,
                 state,
                 package_zip,
                 delivery_time,
                 weight,
                 notes=''):
        self.id = int(package_id)
        self.state = state
        self.address = address
        self.city = city
        self.package_zip = package_zip
        self.delivery_deadline = delivery_time
        self.delivered = False
        self.weight = int(weight)
        self.notes = notes

    # Return package ID.
    def get_id(self):
        return self.id

    # Return package address.
    def get_address(self):
        return self.address

    # Return full address
    def get_full_address(self):
        return f'{self.address}, {self.city}, {self.state} {self.package_zip}'

    # Update package address
    def set_address(self, address, city, state, p_zip):
        self.address = address
        self.city = city
        self.state = state
        self.package_zip = p_zip

    # Return delivery deadline
    def get_delivery_deadline(self):
        return self.delivery_deadline

    # Update delivery deadline
    def set_delivery_deadline(self, d_time):
        self.delivery_deadline = d_time

    # Return delivery status
    def get_delivery_status(self):
        return self.delivered

    # Return weight
    def get_weight(self):
        return self.weight

    # Return package as string
    def to_string(self):
        return f'id: {self.id} address: {self.address}'

    def get_notes(self):
        return self.notes

    # Static method for returning dummy package for HUB
    @staticmethod
    def get_hub():
        return Package(0,
                       'HUB',
                       '',
                       '',
                       '',
                       '',
                       0)
