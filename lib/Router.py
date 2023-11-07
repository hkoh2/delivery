# Router.py

from lib.Package import Package


class Router:

    # Initialize Router for creating routes.
    def __init__(self, package_table, distance_data, address_data):
        self.package_table = package_table
        self.distances = distance_data
        self.addresses = address_data

    # Returns package address by ID
    def get_package_address(self, p_id):
        package = self.package_table.search(p_id)
        return f'{package.get_address()}, {package.city}, {package.state} {package.package_zip}'

    # Routes packages using greedy algorithm
    def route(self, packages):

        # Checks for any empty packages
        if not packages:
            return []

        # Single package on truck is not routed
        if len(packages) == 1:
            return packages

        # Holds packages in the order of delivery
        route = []

        # Dummy package for the HUB
        hub = Package.get_hub()

        # Inserts Dummy package as first to route starting at the HUB
        packages.insert(0, hub)

        # Inserts Dummy package at the end to return the truck to the HUB
        packages.append(hub)

        # Set the starting and next destination to search for shortest distance
        start_location = packages.pop(0)
        next_location = packages[0]
        shortest = 10000
        remove_index = 0

        # Iterate until no more packages are available
        while len(packages) > 1:
            # Iterate all possible destination for shortest distance
            for i, package in enumerate(packages):

                # Get address of the packages for distance
                start_address = start_location.get_address()
                next_address = package.get_address()
                dist = self.get_distance(start_address, next_address)

                # Update the shortest distance if current starting and next
                # location is shorter
                if dist < shortest:
                    shortest = dist
                    next_location = package
                    remove_index = i
            route.append(next_location)
            # reset shortest once the shortest path is found for next package
            shortest = 10000
            # Remove packages that have been routed
            del packages[remove_index]
            next_location = packages[0]
            remove_index = 0
        route.append(next_location)
        del packages[0]
        route.append(hub)

        return route

    # Returns distance between two addresses
    def get_distance(self, start: str, end: str) -> int:
        # Looks up address of packages by index on the addresses list
        first_index = self.addresses.index(start)
        second_index = self.addresses.index(end)
        start_index = max(first_index, second_index)
        end_index = min(first_index, second_index)

        return self.distances[start_index][end_index]

    # Returns hash table of packages
    def get_package_table(self):
        return self.package_table

    # Look up package details by ID
    def lookup_package(self, p_id):
        return self.get_package_table().search(p_id)
