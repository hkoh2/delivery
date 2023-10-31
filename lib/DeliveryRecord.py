# DeliveryRecord.py

class DeliveryRecord:

    def __init__(self, id, distance, time):
        # package id
        self.id = id
        # distance from previous destination
        self.distance = distance
        # time delivered
        self.time = time

    def get_time(self):
        return self.time

    def set_time(self, d_time):
        self.time = d_time

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def get_id(self):
        return self.id