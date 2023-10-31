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
                 notes=''):
        self.id = int(package_id)
        self.state = state
        self.address = address
        self.city = city
        self.package_zip = package_zip
        self.delivery_time = delivery_time
        self.weight = int(weight)
        self.notes = notes

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address

    def get_delivery_time(self):
        return self.delivery_time

    def set_delivery_time(self, d_time):
        self.delivery_time = d_time

    def get_weight(self):
        return self.weight

    @staticmethod
    def get_hub():
        return Package(0,
                       'HUB',
                       '',
                       '',
                       '',
                       '',
                       0)