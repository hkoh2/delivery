# Truck.py


from pprint import pprint
from lib.Package import Package
from typing import List
from datetime import datetime, timedelta


class Truck:
    # Max packages allowed on truck
    MAX_PACKAGES = 16

    # Initialize truck with packages and status
    def __init__(self, truck_id, p_ids=None, p_table=None):
        # Pending if no truck drivers are avialable
        self.was_pending: bool = True
        self.driver: bool = False

        # Truck speed
        self.MPH = 18
        self.MPM = self.MPH / 18.0  # every tick (minute) truck goes 0.3 miles

        # Truck details
        self.id = truck_id
        self.total_distance = 0
        current_time = datetime.today()
        self.departure_time = current_time.replace(hour=8, minute=0, second=0)
        self.destination_distance = 0

        # Packages loaded on the truck
        self.package_ids = p_ids
        self.packages: List[type[Package]] = []
        self.route = []
        self.delivered = []  # tuple with package id and time delivered
        self.delivery_log = None

    # Return total distance traveled by truck.
    def get_total_distance(self):
        total = 0
        for record in self.delivery_log:
            total += record.get_distance()
        return total

    def get_distance_last(self):
        total = 0
        for record in self.delivery_log[:-1]:
            total += record.get_distance()
        return total

    # Return total weight of packages
    def get_weight(self):
        total = 0
        for package in self.route:
            total += package.get_weight()
        return total

    # Return total time taken for delivery
    def get_total_time(self):
        total_time = 0
        for log in self.delivery_log:
            total_time += log.get_minutes()
        return total_time

    # Print delivery records for the truck
    def print_all_records(self, p_table):
        total_distance = 0
        total_time = 0
        total_weight = 0
        print(f'Delivery Record - Truck {self.get_id()}')
        departure_time = self.get_departure()
        print('')
        print(f'  ID - ADDRESS' + ' ' * 34 + '|    DISTANCE |   WEIGHT |        TIME |  DELIVERED | DELIVER BY |')
        print('-' * 123)
        for record in self.get_delivery_log()[:-1]:

            # Total values for packages and delivery
            p_id = record.get_id()
            p_time = record.get_minutes()
            p_distance = record.get_distance()
            p_weight = record.get_weight()
            total_distance += p_distance
            total_time += p_time
            total_weight += p_weight
            package = p_table.search(p_id)
            address = package.get_address()
            delivery_time = package.get_delivery_deadline()
            delivered_time = record.get_time().strftime("%H:%M:%S")
            on_time = True
            on_time_msg = ''

            # Updates delivery status by time
            if delivery_time not in ['EOD', '']:
                delivery_time = (datetime
                                 .strptime(delivery_time, '%H:%M %p')
                                 .strftime("%H:%M:%S"))
                on_time = delivery_time > delivered_time
            if address == 'HUB':
                on_time_msg = ''
            else:
                on_time_msg = 'On time' if on_time else 'Late'
            print(f'{p_id : >4} - {address: <40} | '
                  f'{p_distance : >5} miles | '
                  f'{p_weight : >5.1f} kg | '
                  f' {p_time : >6.2f} min | '
                  f'{delivered_time : >10} | '
                  f'{delivery_time : >10} | '
                  f'{on_time_msg : <8} '
                  )

        print('-' * 123)
        print(f'  TOTAL' + ' ' * 41 + f'| {total_distance : >5.1f} miles |'
              f' {total_weight : >5.1f} kg |  {total_time : >6.2f} min |  '
              f'          |            |'
              )
        end_time = departure_time + timedelta(minutes=total_time)
        print('')
        print(f'Departure: {departure_time.strftime("%H:%M:%S")} - Arrival: {end_time.strftime("%H:%M:%S")}')
        print('\n')

    # Updates delivery log
    def set_delivery_log(self, d_log):
        self.delivery_log = d_log

    # Returns all delivery records
    def get_delivery_log(self):
        return self.delivery_log

    # Return departure time of the truck
    def get_departure(self):
        return self.departure_time

    # Updates departure time for the truck
    def set_departure(self, departure_time):
        self.departure_time = departure_time

    # Returns truck id
    def get_id(self):
        return self.id

    # Load single package to the truck.
    def load_package(self, package):
        if len(self.packages) <= type(self).MAX_PACKAGES:
            self.packages.append(package)
        else:
            raise Exception('Max packages')

    # Load packages by IDs
    def load_packages(self, p_table):
        for p_id in self.package_ids:
            self.load_package(p_table.search(p_id))

    # Get packages loaded on the truck. Not routed.
    def get_packages(self):
        return self.packages

    # Get package routes
    def get_route(self):
        return self.route

    # Load packages by delivery order
    def load_route(self, route):
        self.route = route
