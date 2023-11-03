# Truck.py


from pprint import pprint
from lib.Package import Package
from typing import List
from datetime import datetime, timedelta


class Truck:
    MAX_PACKAGES = 16

    def __init__(self, truck_id, p_ids=None, p_table=None):
        # need to set a different departure time
        self.was_pending: bool = True
        self.MPH = 18
        self.MPM = self.MPH / 18.0  # every tick (minute) truck goes 0.3 miles
        self.id = truck_id
        self.package_ids = p_ids
        self.packages: List[type[Package]] = []
        self.route = []
        self.delivered = []  # tuple with package id and time delivered
        self.delivery_log = None
        self.driver: bool = False
        self.total_distance = 0
        self.destination_distance = 0
        current_time = datetime.today()
        self.departure_time = current_time.replace(hour=8, minute=0, second=0)

    def print_all_records(self, p_table):
        total_distance = 0
        total_time = 0
        print(f'Delivery Record - Truck {self.get_id()}')
        print('------------------------------------------')
        departure_time = self.get_departure()
        print(f'Departure time: {departure_time.strftime("%H:%M:%S")}')

        print(f'  ID - ADDRESS' + ' ' * 34 + '|    DISTANCE |        TIME |  DELIVERED | DELIVER BY |')
        print('-' * 111)
        for record in self.get_delivery_log():
            p_id = record.get_id()
            p_time = record.get_minutes()
            p_distance = record.get_distance()
            total_distance += p_distance
            total_time += p_time
            package = p_table.search(p_id)
            address = package.get_address()
            delivery_time = package.get_delivery_time()
            delivered_time = record.get_time().strftime("%H:%M:%S")
            on_time = True
            on_time_msg = ''
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
                  f' {p_time : >6.2f} min | '
                  f'{delivered_time : >10} | '
                  f'{delivery_time : >10} | '
                  f'{on_time_msg : <8} '
                  )

        print(f'\nTotal time: {total_time : >6.2f} min | Total distance: {total_distance : >5.1f} miles')
        end_time = departure_time + timedelta(minutes=total_time)
        print(f'Arrival at HUB: {end_time.strftime("%H:%M:%S")}')
        print('\n')

    def set_delivery_log(self, d_log):
        self.delivery_log = d_log

    def get_delivery_log(self):
        return self.delivery_log

    def get_departure(self):
        return self.departure_time

    def set_departure(self, departure_time):
        self.departure_time = departure_time

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