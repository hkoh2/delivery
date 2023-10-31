# Router.py

from lib.Package import Package

class Router:

    def __init__(self, package_table, distance_data, address_data):
        self.package_table = package_table
        self.distances = distance_data
        self.addresses = address_data

    def route(self, packages):

        print(f'Packages to be routed - {[p.get_id() for p in packages]}')

        if not packages:
            return []
        if len(packages) == 1:
            return packages

        route = []

        # TODO: start location should be HUB!!!!

        # TODO: HUB has id 0 <- start with this instead of a real package

        hub = Package.get_hub()

        packages.insert(0, hub)
        packages.append(hub)
        start_location = packages.pop(0)

        # print(packages)
        if len(packages) < 2:
            return route

        shortest = 10000
        next_location = packages[0]
        remove_index = 0

        while len(packages) > 1:
            for i, package in enumerate(packages):
                start_address = start_location.get_address()
                next_address = package.get_address()
                dist = self.get_distance(start_address, next_address)
                if dist < shortest:
                    shortest = dist
                    next_location = package
                    remove_index = i

            # print("shortest - ", shortest)
            route.append(next_location)
            shortest = 10000
            del packages[remove_index]
            next_location = packages[0]
            remove_index = 0
        route.append(next_location)
        del packages[0]
        route.append(hub)

        print(f'Routed packages       - {[p.get_id() for p in route]}')
        print('')
        return route

    # Returns distance between two addresses
    def get_distance(self, start: str, end: str) -> int:
        first_index = self.addresses.index(start)
        second_index = self.addresses.index(end)
        start_index = max(first_index, second_index)
        end_index = min(first_index, second_index)

        return self.distances[start_index][end_index]

    def get_package_table(self):
        return self.package_table