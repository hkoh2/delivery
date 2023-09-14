# Package.py

class Package:
    def __init__(self,
                 package_id,
                 address,
                 city,
                 state,
                 package_zip,
                 delivery_time,
                 weight,
                 notes):
        self.id = package_id
        self.state = state
        self.address = address
        self.city = city
        self.package_zip = package_zip
        self.delivery_time = delivery_time
        self.weight = weight
        self.notes = notes


