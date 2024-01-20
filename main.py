# main.py

# Student ID - 010262309
# Name - Han Koh
# WGUPS ROUTING PROGRAM

import csv
from lib.Hash import ChainingHashTable
from lib.Package import Package
from lib.Truck import Truck
from lib.Router import Router
from lib.Dispatcher import Dispatcher
from datetime import datetime, timedelta
import os


def clear_screen():
    # clears screen for terminal
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


if __name__ == '__main__':

    # Initialize lists to keep track of trucks and package ids
    active_trucks = []
    package_ids = []

    # Hash table for looking up packages by ID
    packages_table = ChainingHashTable()

    # read csv to package and add to hash table.
    with open('./csv/package.csv', mode='r') as file:
        packageFile = csv.reader(file)

        # Inserts Package objects to hash table by ID
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

    # Read from csv to parse address and distance for use with routing
    with open('./csv/distances.csv', mode='r') as file:
        distanceFile = csv.reader(file)
        for distance in distanceFile:

            # Parsing address from csv
            address = distance[1].split('\n')[0].strip()
            address_data.append(address)

            # Convert string to float for distance
            distance_clean = [0 if val == '' else float(val) for val in distance[2:]]
            distance_data.append(distance_clean)

    # Manually load packages by ID to be loaded on to the truck
    truck1_package_ids = ([14, 15, 19, 16, 13, 20] +
                          [29, 30, 31, 34, 37])
    truck1 = Truck(1, truck1_package_ids, packages_table)
    active_trucks.append(truck1)

    truck2_package_ids = ([3, 18, 36, 38] +
                           [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 40, 25])
    truck2 = Truck(2, truck2_package_ids, packages_table)
    # Adjusting departure time of truck 2
    truck2.set_departure(datetime.today().replace(hour=9, minute=5, second=0))
    active_trucks.append(truck2)

    # address needs to be updated for 9
    truck3_package_ids = [28, 32, 9] + [17, 21, 22, 23, 24, 26, 27, 33, 35, 39]
    truck3 = Truck(3, truck3_package_ids, packages_table)
    active_trucks.append(truck3)

    # Updating address for package
    updated_package = packages_table.search(9)
    updated_package.set_address(
        '410 S State St',
        'Salt Lake City',
        'UT',
        '84111'
    )

    # All package IDs loaded on the trucks
    all_packages = truck1_package_ids + truck2_package_ids + truck3_package_ids

    # Router instance that routes and keeps package data.
    router = Router(packages_table, distance_data, address_data)

    # Dispatcher assigns driver and sends out trucks for delivery
    dispatcher = Dispatcher(active_trucks, router, 2)
    dispatcher.generate_route()
    dispatcher.dispatch_routes()

    # Interactive terminal
    running = True
    clear_screen()
    print('WGUPS ROUTING PROGRAM')
    print('')
    while running:
        # Options in the terminal
        print('')
        print('1. Show delivery records for all packages')
        print('2. Show delivery records for all packages by truck')
        print('3. Show all packages by time')
        print('4. Overview of delivery trucks')
        print('5. Specific package delivery status by time')
        print('0. Exit')
        user_input = input("Choose an option from above: ")

        match user_input:
            case '0':
                # 0. Exit
                running = False
            case '1':
                # 1. Show delivery records for all packages
                clear_screen()
                updated_package = packages_table.search(9)
                updated_package.set_address(
                    '410 S State St',
                    'Salt Lake City',
                    'UT',
                    '84111'
                )
                # Display delivery records of all packages
                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()
                dispatcher.get_complete_log()
            case '2':
                # 2. Show delivery records for all packages by truck
                clear_screen()
                trucks_text = ' '.join([str(truck.get_id()) for truck in active_trucks])
                print(f'Available truck ids: {trucks_text}')
                truck_selected = input(f'Enter truck id (0 for all trucks): ')
                clear_screen()
                updated_package = packages_table.search(9)
                updated_package.set_address(
                    '410 S State St',
                    'Salt Lake City',
                    'UT',
                    '84111'
                )
                # Display delivery records by trucks
                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()
                dispatcher.get_delivery_log(int(truck_selected))
            case '3':
                # 3. Show all packages by time
                clear_screen()
                # Some default values to choose from
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
                # Convert time for comparison
                time_entered = (datetime
                                .strptime(time_input, '%H:%M')
                                .strftime("%H:%M:%S"))
                update_time = (datetime
                               .strptime('10:20', '%H:%M')
                               .strftime("%H:%M:%S"))

                # If separates package by selected time
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

                # Display all package status by time
                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()
                dispatcher.get_log_by_time(time_entered)
            case '4':
                # 4. Overview of delivery trucks
                clear_screen()
                print(f'Overview of trucks and packages\n')

                # Initialize total values for display
                delivery_total_distance = 0
                delivery_total_distance_last = 0
                delivery_total_packages = 0
                delivery_total_time = 0
                delivery_total_weight = 0
                departures = []
                arrivals = []

                for truck in active_trucks:
                    # Find total values of individual trucks for each category
                    t_id = truck.get_id()
                    total_packages = len(truck.get_route()) - 2  # remove HUB
                    total_weight = truck.get_weight()
                    total_time = truck.get_total_time()
                    total_distance = truck.get_total_distance()
                    total_distance_last = truck.get_distance_last()

                    # Total values of all trucks and packages
                    delivery_total_weight += total_weight
                    delivery_total_packages += total_packages
                    delivery_total_time += total_time
                    delivery_total_distance += total_distance
                    delivery_total_distance_last += total_distance_last

                    # Time conversion for formatting
                    hr = int(total_time / 60)
                    minute = int(total_time % 60)
                    departure_time = truck.get_departure()
                    arrival_time = departure_time + timedelta(minutes=total_time)
                    departures.append(departure_time)
                    arrivals.append(arrival_time)

                    # Individual truck values
                    print(f'Truck {t_id} - Packages: {total_packages} | '
                          f'Weight: {total_weight} kg | '
                          f'Departure: {departure_time.strftime("%H:%M")} | '
                          f'Arrival: {arrival_time.strftime("%H:%M")} | '
                          f'Time taken: {hr}:{minute :02d} | '
                          f'Total distance: {total_distance_last : .1f} miles  | '
                          )
                print('-' * 127)

                d_hr = int(delivery_total_time / 60)
                d_minute = int(delivery_total_time % 60)

                earliest = min(departures)
                last = max(arrivals)

                # Total values display for all trucks and packages
                print(f'Total   - Packages: {delivery_total_packages} | '
                      f'Weight: {delivery_total_weight} kg | '
                      f'Departure: {earliest.strftime("%H:%M")} | '
                      f'Arrival: {last.strftime("%H:%M")} | '
                      f'Time taken: {d_hr}:{d_minute} | '
                      f'Total distance: {delivery_total_distance_last : .1f} miles | '
                      )

                # Shows the earliest departure time and latest arrival time.
                time_diff = last - earliest
                sec = time_diff.total_seconds()
                print(' ' * 75 + ' | Dep to Arr: {:1}:{:02}'.format(int(sec / 3600), int(sec % 3600 // 60)) + ' |')

            case '5':
                # 5. Package details
                clear_screen()

                # Get user input for package ID
                print('Package details\n')
                p_id = input('Enter package id: ')

                # Check for invalid values
                if not p_id.isdigit():
                    input("Invalid input. Please enter to continue")
                    clear_screen()
                    continue

                p_id = int(p_id)

                # check for invalid ids
                if p_id not in all_packages:
                    input('ID not found. Press enter to continue')
                    clear_screen()
                    continue

                p_time = input('Enter time (HH:MM): ')

                # validate time input
                try:
                    time_entered = (datetime
                                    .strptime(p_time, '%H:%M')
                                    .strftime("%H:%M:%S"))
                except ValueError:
                    input('Invalid time. Press enter to continue.')
                    continue

                update_time = (datetime
                               .strptime('10:20', '%H:%M')
                               .strftime("%H:%M:%S"))

                # If separates package by selected time
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

                # Display all package status by time
                dispatcher = Dispatcher(active_trucks, router, 2)
                dispatcher.generate_route()
                dispatcher.dispatch_routes()
                print(dispatcher.get_package_detail(p_id, time_entered))
                print('')
            case _:
                clear_screen()
                pass
