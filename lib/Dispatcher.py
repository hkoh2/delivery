# Dispatcher.py

from lib.DeliveryRecord import DeliveryRecord


class Dispatcher:

    def __init__(self, trucks, router, driver_count, drivers=2):
        self.driver_count = driver_count
        # router
        self.router = router
        # active trucks
        self.trucks = trucks
        # dispatched trucks
        self.active = []
        # pending dispatch
        self.pending = []
        self.finished = []
        self.time = 0
        # number of drivers available
        self.drivers = drivers

    def trucks_update(self):
        pass

    def dispatch_trucks(self):
        pass

    def load_router(self, router):
        """Router for distance"""
        self.router = router

    def generate_route(self):
        """Start"""

        print("")
        print("\033[94m --- Routing packages --- \033[0m")
        print(" * Routes packages using greedy algo based on distance")
        print("")

        # need to assign driver

        # while self.active and self.pending:
        for truck in self.trucks:
            # Add ID and time of delivered packages into each truck.
            #print(f'Departure time: {truck.get_departure()}')
            pack_to_be_routed = truck.get_packages()
            routed = self.router.route(truck.get_packages())
            truck.load_route(routed)

        print("\033[94m --- Finished routing packages  --- \033[0m")

    def end(self):
        return not self.active and not self.pending

    def tick(self):
        self.time += 1
        """ TODO: Need to check with trucks for update
                  on where the location is
        """
        self.trucks_update()

    def update_delivery_address(self, p_id, p_address):
        pass

    def deliver(self, truck):
        print(f'*** Truck {truck.get_id()} ***')
        delivery_log = []
        # start_location = 'HUB'
        end_location = 'HUB'
        # Time delivered
        # [DeliveryRecord, ...]
        total_distance = 0
        total_time = 0
        route = truck.get_route()
        start_location = route[0].get_address()
        for package in route:
            pack_address = package.get_address()
            distance = self.router.get_distance(start_location, pack_address)
            total_distance += distance
            time = 10 / 3.0 * distance
            total_time += time
            print(f'distance - {distance} miles, time - {time} min')
            delivery_record = DeliveryRecord(package.get_id(), distance, time)
            delivery_log.append(delivery_record)
            start_location = pack_address

        print(f'total distance - {total_distance}')
        print(f'total time     - {total_time}')
        print('')
        truck.set_delivery_log(delivery_log)
        return truck

    """
    Dispatches truck for delivery
    """
    def dispatch_routes(self):

        # assign available drivers to truck
        # self.trucks should have truck in order by departure time
        active_drivers = self.drivers
        index = 0
        for i, truck in enumerate(self.trucks):
            if active_drivers < 1:
                self.pending = self.trucks[i:]
                break
            truck.driver = True
            active_drivers -= 1
            self.active.append(truck)

        print(f'active  - {len(self.active)}')
        print(f'pending - {len(self.pending)}')

        # while self.active or self.pending
        """
        TODO: we don't know who will finish first when the delivery is complete.
        will need to go through the lo
        """

        # keep routing until active queue is empty
        # check pending queue for any trucks after finished.

        while self.active:
            current_truck = self.active[0]
            self.deliver(current_truck)
            self.finished.append(current_truck)
            del self.active[0]
            if self.pending:
                print(f'Moving truck {self.pending[0].get_id()} to active queue')
                self.active.append(self.pending[0])
                del self.pending[0]

        print('')

    def get_delivery_log(self):
        for truck in self.trucks:
            total_distance = 0
            total_time = 0
            print(f'Delivery Record - Truck {truck.get_id()}')
            print('------------------------------------------')

            for record in truck.get_delivery_log():
                p_table = self.router.get_package_table()
                p_id = record.get_id()
                p_time = record.get_time()
                p_distance = record.get_distance()
                total_distance += p_distance
                total_time += p_time
                address = p_table.search(p_id).get_address()
                print(f'{p_id : >4} - {address: <25} - {p_time : >6.2f} min {p_distance : >5} miles')

            print(f'\nTotal time: {total_time : >6.2f} min | Total distance: {total_distance : >5} miles')
            print('\n')
            total_distance = 0
            total_time = 0

    def get_delivery_log_by_time(self, start_time, end_time):
        # if package is delivered, packages should not be on the truck
        pass

    def status(self):
        print(f"trucks   - {[t.get_id() for t in self.trucks]}")
        print(f"pending  - {self.pending}")
        print(f"active   - {self.active}")
        print(f"finished - {self.finished}")
