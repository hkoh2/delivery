# Truck.py


from pprint import pprint
from lib.Package import Package
from typing import List
from datetime import datetime


class Truck:
    MAX_PACKAGES = 16

    def __init__(self, truck_id, p_ids=None):
        self.MPH = 18
        self.MPM = self.MPH / 18.0  # every tick (minute) truck goes 0.3 miles
        self.id = truck_id
        self.package_ids = p_ids
        self.packages: List[type[Package]] = []
        self.route = []
        self.delivered = []  # tuple with package id and time delivered
        self.delivery_log = None
        self.driver = False
        self.total_distance = 0
        self.destination_distance = 0
        current_time = datetime.today()
        # current_time.replace(hour=8, minute=0, second=0)
        self.departure_time = current_time.replace(hour=8, minute=0, second=0)

    def set_delivery_log(self, d_log):
        self.delivery_log = d_log

    def get_delivery_log(self):
        return self.delivery_log

    def get_departure(self):
        return self.departure_time

    def update_location(self):
        self.total_distance += self.MPM

    def get_destination(self):
        return self.route[0]

    def get_id(self):
        return self.id

    def get_driver(self):
        return self.driver

    def load_package(self, package):
        if len(self.packages) <= type(self).MAX_PACKAGES:
            self.packages.append(package)
        else:
            raise Exception('Max packages')

    def load_packages(self, p_table):
        for p_id in self.package_ids:
            self.load_package(p_table.search(p_id))

    def unload_package(self, package_id):
        pass

    def get_packages(self):
        return self.packages

    def get_route(self):
        return self.route

    def load_route(self, route):
        self.route = route

    def print_packages(self):
        # pprint(vars(self.packages))
        for pack in self.packages:
            pprint(vars(pack))