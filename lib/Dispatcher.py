# Dispatcher.py

from lib.DeliveryRecord import DeliveryRecord
from datetime import datetime, timedelta


class Dispatcher:

    def __init__(self, trucks, router, driver_count):
        # Available drivers
        self.driver_count = driver_count
        # router for routing packages
        self.router = router
        # active trucks
        self.trucks = trucks
        # dispatched trucks
        self.active = []
        # pending dispatch
        self.pending = []
        # Trucks finished with deliveries
        self.finished = []
        # Time taken for delivery
        self.time = 0
        # number of drivers available
        self.route_end_time = []

    # Return delivery log from all trucks
    def get_all_truck_delivery_log(self):
        records = []
        for truck in self.finished:
            for log in truck.get_delivery_log():
                records.append(log)
        return records

    # Return package detail of a truck by ID
    def get_package_detail(self, p_id, p_time):
        all_records = self.get_all_truck_delivery_log()
        for record in all_records:
            package_id = record.get_id()
            if p_id == package_id:
                delivered_time = record.get_time().strftime("%H:%M:%S")
                status = 'Delivered'
                departure_time = record.get_departure().strftime("%H:%M:%S")
                print('')
                # Need to check the time of delivery
                if p_time < departure_time:
                    status = 'At HUB'
                elif p_time < delivered_time:
                    status = 'En route'
                package = self.router.get_package_table().search(p_id)

                delivered_msg = "N/A" if status != "Delivered" else record.get_time().strftime("%H:%M:%S")
                return (f'ID        : {p_id}\n'
                        f'On truck  : {record.get_truck_id()}\n'
                        f'Address   : {package.get_full_address()}\n'
                        f'Weight    : {package.get_weight()}\n'
                        f'Departure : {record.get_departure().strftime("%H:%M %p")}\n'
                        f'Delivered : {delivered_msg}\n'
                        f'Deliver by: {package.get_delivery_deadline()}\n'
                        f'Status    : {status}\n'
                        f'Notes     : {package.get_notes()}'
                        )

    # Load router
    def load_router(self, router):
        self.router = router

    # Generates routes based on packages loaded on the truck
    def generate_route(self):
        for truck in self.trucks:
            # Load packages to the truck with package details
            truck.load_packages(self.router.get_package_table())
            pack_to_be_routed = truck.get_packages()
            # Routes and loads packages based on shortest distance
            routed = self.router.route(pack_to_be_routed)
            truck.load_route(routed)

    # Delivers packages based on route
    def deliver(self, truck):
        # Delivery logs
        delivery_log = []
        total_distance = 0
        total_time = 0
        route = truck.get_route()
        start_location = route[0].get_address()
        truck_id = truck.get_id()

        # Delivers packages and calculates time and distance from last destination.
        for package in route:
            pack_address = package.get_address()
            distance = self.router.get_distance(start_location, pack_address)
            weight = package.get_weight()
            total_distance += distance

            # Delivery time calculations
            time = 10 / 3.0 * distance
            total_time += time
            delivery_time = truck.get_departure() + timedelta(minutes=total_time)

            # Creates a record of the delivery
            delivery_record = DeliveryRecord(
                truck_id,
                package.get_id(),
                distance,
                time,
                delivery_time,
                truck.get_departure(),
                weight
            )
            delivery_log.append(delivery_record)
            start_location = pack_address

        # Calculates time the truck arrives at the HUB
        end_time = truck.get_departure() + timedelta(minutes=total_time)
        self.route_end_time.append(end_time)
        self.route_end_time.sort()  # Earliest time on index 0

        # Stores delivery log to the truck
        truck.set_delivery_log(delivery_log)
        return truck

    # Dispatches truck for delivery
    def dispatch_routes(self):

        # Assign drivers to the truck.
        # Unassigned trucks are in pending status and does not depart until
        # another driver comes back from delivery.
        active_drivers = self.driver_count
        for i, truck in enumerate(self.trucks):
            # When no more drivers are available all trucks are in pending status.
            if active_drivers < 1:
                self.pending = self.trucks[i:]
                break
            # Assign driver
            truck.driver = True
            truck.was_pending = False
            # Counter for available drivers decreased as trucks are assign drivers.
            active_drivers -= 1
            self.active.append(truck)

        while self.active:
            current_truck = self.active[0]
            # Set departure time if truck was pending for driver
            if current_truck.was_pending:
                current_truck.set_departure(self.route_end_time[0])
                self.route_end_time.pop(0)
            # Deliver package for trucks with drivers
            self.deliver(current_truck)
            # Move truck to finished once delivery is complete.
            self.finished.append(current_truck)
            del self.active[0]

            # assign driver to pending once route finishes
            if self.pending:
                self.active.append(self.pending[0])
                del self.pending[0]

    # Returns delivery log of trucks based on truck ID.
    def get_delivery_log(self, t_id=0):
        # 0 for all trucks
        if t_id == 0:
            for truck in self.finished:
                truck.print_all_records(self.router.get_package_table())
        else:
            for truck in self.finished:
                if truck.get_id() == t_id:
                    truck.print_all_records(self.router.get_package_table())

    # Returns logs of all delivery trucks.
    def get_complete_log(self):
        records = self.get_all_truck_delivery_log()

        # Sorting all packages by time delivered.
        sorted_records = sorted(records, key=lambda r: r.get_time())
        sorted_records = [record for record in sorted_records if record.get_id() is not 0]

        total_distance = 0
        total_minutes = 0

        print('All delivery records\n')
        print(f'TRUCK |  ID - ADDRESS' + ' ' * 34 + '|    DISTANCE |        TIME |  DELIVERED | DELIVER BY |')
        for record in sorted_records:

            # Gathering package information.
            p_id = record.get_id()
            truck_id = record.get_truck_id()
            p_time = record.get_minutes()
            p_distance = record.get_distance()
            total_distance += p_distance
            total_minutes += p_time
            package = self.router.get_package_table().search(p_id)
            address = package.get_address()

            # Time calculation for deadline and delivered time
            delivery_time = package.get_delivery_deadline()
            delivered_time = record.get_time().strftime("%H:%M:%S")
            on_time = True
            on_time_msg = ''

            # Updating status of package based on deadline.
            if delivery_time not in ['EOD', '']:
                delivery_time = (datetime
                                 .strptime(delivery_time, '%H:%M %p')
                                 .strftime("%H:%M:%S"))
                on_time = delivery_time > delivered_time
            if address != 'HUB':
                on_time_msg = 'On time' if on_time else 'Late'
            print(f'{truck_id : >5} |'
                  f'{p_id : >4} - {address: <40} | '
                  f'{p_distance : >5} miles | '
                  f' {p_time : >6.2f} min | '
                  f'{delivered_time : >10} | '
                  f'{delivery_time : >10} | '
                  f'{on_time_msg : <8} '
                  )

    # Returns package and delivery records by time.
    def get_log_by_time(self, time):

        # Gather all records
        records = []
        for truck in self.finished:
            for log in truck.get_delivery_log():
                records.append(log)

        # Sort package by time delivered.
        sorted_records = sorted(records, key=lambda r: r.get_time())
        sorted_records = [record for record in sorted_records if record.get_id() is not 0]

        # Flag for divider for the time entered
        divider_used = False

        print(f'Package status by time - {time}\n')
        print('TRUCK |  ID - ADDRESS' + ' ' * 69 + '|       TIME | DELIVER BY | STATUS')
        for record in sorted_records:
            departure_time = record.get_departure().strftime("%H:%M:%S")
            truck_id = record.get_truck_id()
            p_id = record.get_id()
            if p_id == 0:
                continue
            address = self.router.get_package_address(p_id)
            package = self.router.get_package_table().search(p_id)
            delivery_time = package.get_delivery_deadline()
            distance = record.get_distance()
            distance_travelled = 0
            distance_left = 0

            # Status message for the packages based on time
            msg = ''
            delivered_time = record.get_time().strftime("%H:%M:%S")
            if departure_time > time:
                # truck at hub
                msg = 'At HUB'
                distance_left += distance
            elif delivered_time > time:
                # not delivered
                msg = 'En route'
                distance_left += distance
            else:
                msg = 'Delivered'
                distance_travelled += distance

            # Setting divider for the time entered.
            if not divider_used and delivered_time > time:
                print(f'----------- {time} -----------' * 4)
                divider_used = True

            print(f'{truck_id : >5} |'
                  f'{p_id : >4} - {address: <75} | '
                  f'{delivered_time : >10} | '
                  f'{delivery_time : >10} | '
                  f'{msg : <10} '
                  )
