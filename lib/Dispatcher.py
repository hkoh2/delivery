# Dispatcher.py

from lib.DeliveryRecord import DeliveryRecord
from datetime import datetime, timedelta


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
        self.route_end_time = []

    def get_all_truck_delivery_log(self):
        records = []
        for truck in self.finished:
            for log in truck.get_delivery_log():
                records.append(log)
        return records

    def get_package_detail(self, p_id):
        all_records = self.get_all_truck_delivery_log()
        for record in all_records:
            package_id = record.get_id()
            if p_id == package_id:
                package = self.router.get_package_table().search(p_id)
                return (f'ID        : {p_id}\n'
                        f'On truck  : {record.get_truck_id()}\n'
                        f'Address   : {package.get_full_address()}\n'
                        f'Weight    : {package.get_weight()}\n'
                        f'Delivered : {record.get_time().strftime("%H:%M %p")}\n'
                        f'Deliver by: {package.get_delivery_deadline()}'
                        )

    def load_router(self, router):
        self.router = router

    def generate_route(self):
        for truck in self.trucks:
            truck.load_packages(self.router.get_package_table())
            pack_to_be_routed = truck.get_packages()
            routed = self.router.route(pack_to_be_routed)
            truck.load_route(routed)

    def deliver(self, truck):
        delivery_log = []
        total_distance = 0
        total_time = 0
        route = truck.get_route()
        start_location = route[0].get_address()
        truck_id = truck.get_id()

        for package in route:
            pack_address = package.get_address()
            distance = self.router.get_distance(start_location, pack_address)
            weight = package.get_weight()
            total_distance += distance
            time = 10 / 3.0 * distance
            total_time += time
            delivery_time = truck.get_departure() + timedelta(minutes=total_time)
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

        end_time = truck.get_departure() + timedelta(minutes=total_time)
        self.route_end_time.append(end_time)
        self.route_end_time.sort()  # Earliest time on index 0

        truck.set_delivery_log(delivery_log)
        return truck

    """
    Dispatches truck for delivery
    """
    def dispatch_routes(self):
        active_drivers = self.drivers
        for i, truck in enumerate(self.trucks):
            if active_drivers < 1:
                self.pending = self.trucks[i:]
                break
            truck.driver = True
            truck.was_pending = False
            active_drivers -= 1
            self.active.append(truck)

        while self.active:
            current_truck = self.active[0]
            # Set departure time if truck was pending for driver
            if current_truck.was_pending:
                current_truck.set_departure(self.route_end_time[0])
                self.route_end_time.pop(0)
            # Deliver package
            self.deliver(current_truck)
            self.finished.append(current_truck)
            del self.active[0]

            # assign driver to pending once route finishes
            if self.pending:
                self.active.append(self.pending[0])
                del self.pending[0]

    def get_delivery_log(self, t_id=0):
        if t_id == 0:
            for truck in self.finished:
                truck.print_all_records(self.router.get_package_table())
        else:
            for truck in self.finished:
                if truck.get_id() == t_id:
                    truck.print_all_records(self.router.get_package_table())

    def get_complete_log(self):
        records = self.get_all_truck_delivery_log()

        sorted_records = sorted(records, key=lambda r: r.get_time())
        sorted_records = [record for record in sorted_records if record.get_id() is not 0]
        total_distance = 0
        total_minutes = 0

        print('All delivery records\n')
        print(f'TRUCK |  ID - ADDRESS' + ' ' * 34 + '|    DISTANCE |        TIME |  DELIVERED | DELIVER BY |')
        for record in sorted_records:

            p_id = record.get_id()
            truck_id = record.get_truck_id()
            p_time = record.get_minutes()
            p_distance = record.get_distance()
            total_distance += p_distance
            total_minutes += p_time
            package = self.router.get_package_table().search(p_id)
            address = package.get_address()
            delivery_time = package.get_delivery_deadline()
            delivered_time = record.get_time().strftime("%H:%M:%S")
            on_time = True
            on_time_msg = ''
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

    def get_log_by_time(self, time):
        records = []
        for truck in self.finished:
            for log in truck.get_delivery_log():
                records.append(log)

        sorted_records = sorted(records, key=lambda r: r.get_time())
        sorted_records = [record for record in sorted_records if record.get_id() is not 0]
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
            if not divider_used and delivered_time > time:
                print(f'----------- {time} -----------' * 4)
                divider_used = True

            print(f'{truck_id : >5} |'
                  f'{p_id : >4} - {address: <75} | '
                  f'{delivered_time : >10} | '
                  f'{delivery_time : >10} | '
                  f'{msg : <10} '
                  )

    def status(self):
        print(f"trucks   - {[t.get_id() for t in self.trucks]}")
        print(f"pending  - {self.pending}")
        print(f"active   - {self.active}")
        print(f"finished - {[i.get_id() for i in self.finished]}")
