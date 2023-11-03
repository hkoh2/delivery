# DeliveryRecord.py

from datetime import datetime, timedelta


class DeliveryRecord:

    def __init__(self, truck_id, p_id, distance, minutes, d_time, departure):
        # truck id
        self.truck_id = truck_id
        # package id
        self.id = p_id
        # distance from previous destination
        self.distance = distance
        # time delivered
        self.minutes = minutes
        self.delivery_time = d_time
        self.departure = departure
        self.last = False

    def get_truck_id(self):
        return self.truck_id

    def get_time(self):
        return self.delivery_time

    def get_minutes(self):
        return self.minutes

    def get_delivery_time(self):
        return self.delivery_time

    def set_minutes(self, d_time):
        self.minutes = d_time

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def get_id(self):
        return self.id

    def get_truck_id(self):
        return self.truck_id

    def get_departure(self):
        return self.departure

    def to_string(self) -> str:
        pass
