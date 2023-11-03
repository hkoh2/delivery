# main.py

# Student ID -
# Name - Han Koh
# WGUPS ROUTING PROGRAM

import csv
from lib.Hash import ChainingHashTable
from lib.Package import Package
from lib.Truck import Truck
from lib.Router import Router
from lib.Dispatcher import Dispatcher
from datetime import datetime
import os


def clear_screen():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


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

    truck1_package_ids = ([14, 15, 19, 16, 13, 20] +
                          [29, 30, 31, 34, 37])
    truck1 = Truck(1, truck1_package_ids, packages_table)
    active_trucks.append(truck1)

    truck2_package_ids = ([3, 18, 36, 38] +
                          [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 40, 25])
    truck2 = Truck(2, truck2_package_ids, packages_table)
    truck2.set_departure(datetime.today().replace(hour=9, minute=5, second=0))
    active_trucks.append(truck2)

    # address needs to be updated for 9
    truck3_package_ids = [28, 32, 9] + [17, 21, 22, 23, 24, 26, 27, 33, 35, 39]
    truck3 = Truck(3, truck3_package_ids, packages_table)
    active_trucks.append(truck3)

    updated_package = packages_table.search(9)
    updated_package.set_address(
        '410 S State St',
        'Salt Lake City',
        'UT',
        '84111'
    )

    all_packages = truck1_package_ids + truck2_package_ids + truck3_package_ids
    counted = []
    wtf = []
    for i in all_packages:
        if i not in counted:
            counted.append(i)
        else:
            wtf.append(i)

    for truck in active_trucks:
        print(f'truck {truck.get_id()} has {len(truck.package_ids)} packages')

    router = Router(packages_table, distance_data, address_data)

    dispatcher = Dispatcher(active_trucks, router, 2)
    dispatcher.generate_route()
    dispatcher.dispatch_routes()

    all_package_ids = [i for i in range(1, 41)]
    routed_packages = truck1_package_ids + truck2_package_ids + truck3_package_ids
    remaining_packages = [i for i in all_package_ids if i not in routed_packages]

    user_input = input("Press Enter to continue.")
    running = True
    print('WGUPS ROUTING PROGRAM')
    print('')
    print(f'Total number of packages: {len(all_packages)}')
    while running:
        # Name of app
        clear_screen()
        print('')
        print('1. Show delivery records for all packages')
        print('1. Show delivery records for all packages by truck')
        print('3. Show all packages by time')
        print('4. Overview - TODO')
        print('0. Exit')
        user_input = input("Choose an option from above: ")

        match user_input:
            case '0':
                running = False
            case '1':
                clear_screen()
                updated_package = packages_table.search(9)
                updated_package.set_address(
                    '410 S State St',
                    'Salt Lake City',
                    'UT',
                    '84111'
                )
                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()
                dispatcher.get_complete_log()
            case '2':
                clear_screen()
                updated_package = packages_table.search(9)
                updated_package.set_address(
                    '410 S State St',
                    'Salt Lake City',
                    'UT',
                    '84111'
                )
                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()
                dispatcher.get_delivery_log()
            case '3':
                clear_screen()
                print(f'1. 9:00')
                print(f'2. 10:00')
                print(f'3. 12:30')
                time_input = input("Or enter time (HH:MM): ")
                clear_screen()

                if time_input == '1':
                    time_input = '9:00'
                elif time_input == '2':
                    time_input = '10:00'
                elif time_input == '3':
                    time_input = '12:30'
                time_entered = (datetime
                                .strptime(time_input, '%H:%M')
                                .strftime("%H:%M:%S"))
                update_time = (datetime
                               .strptime('10:20', '%H:%M')
                               .strftime("%H:%M:%S"))

                if time_entered > update_time:
                    updated_package = packages_table.search(9)
                    updated_package.set_address(
                        '410 S State St',
                        'Salt Lake City',
                        'UT',
                        '84111'
                    )
                else:
                    updated_package = packages_table.search(9)
                    updated_package.set_address(
                        '300 State St',
                        'Salt Lake City',
                        'UT',
                        '84103'
                    )

                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()

                dispatcher.get_log_by_time(time_entered)
            case _:
                clear_screen()
                pass
