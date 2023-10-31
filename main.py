# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
from pprint import pprint
from lib.Hash import ChainingHashTable
from lib.Package import Package
from lib.Truck import Truck
from lib.Router import Router
from lib.Dispatcher import Dispatcher




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    test_pack = Package.get_hub()

    active_trucks = []

    package_ids = []

    packages_table = ChainingHashTable()

    # read csv to package and add to hash table.
    with open('./csv/package.csv', mode='r') as file:
        packageFile = csv.reader(file)
        for package in packageFile:
            new_package = Package(*package)
            # pprint(vars(new_package))
            p_index = int(package[0])
            packages_table.insert(p_index, new_package)
            package_ids.append(p_index)

    # Dummy package for HUB
    hub = Package(0,
                  'HUB',
                  '',
                  '',
                  '',
                  '',
                  '0')
    packages_table.insert(0, hub)

    address_data = []
    distance_data = []
    with open('./csv/distances.csv', mode='r') as file:
        distanceFile = csv.reader(file)
        for distance in distanceFile:

            address = distance[1].split('\n')[0].strip()
            address_data.append(address)

            distance_clean = [0 if val == '' else float(val) for val in distance[2:]]
            distance_data.append(distance_clean)

    # -------------------------------------------------------------------------
    # *** How to look up distance.
    # Get index of two location from address_data i.e address_data.index()
    # always start with bigger index - i.e. distance_data(max(a, b), min(a, b))
    # -------------------------------------------------------------------------

    truck1_package_ids = [1, 11, 17, 23, 31, 32, 33]
    truck1 = Truck(1, truck1_package_ids)
    active_trucks.append(truck1)

    truck2_package_ids = [2, 13, 16, 18, 19, 20, 36, 37, 38]
    truck2 = Truck(2, truck2_package_ids)
    active_trucks.append(truck2)

    truck3_package_ids = [3, 4, 5, 10, 40]
    truck3 = Truck(3, truck3_package_ids)
    active_trucks.append(truck3)

    for truck in active_trucks:
        truck.load_packages(packages_table)

    print("remaining packages")
    print(package_ids)

    router = Router(packages_table, distance_data, address_data)

    dispatcher = Dispatcher(active_trucks, router, 2)

    dispatcher.generate_route()
    dispatcher.dispatch_routes()
    dispatcher.update_delivery_address(1, '')
    dispatcher.get_delivery_log()

    dispatcher.status()


