import mesa



class Route():

    def __init__(self, capacity=5, route_length=3):
        self.capacity = capacity
        self.vehicle_queue = []
        self.route_length = route_length


    def accept_vehicle(self, vehicle):
        print(vehicle)
        if len(self.vehicle_queue) <= self.capacity:
            self.vehicle_queue.append(vehicle)
            print(self.vehicle_queue)
            return True
        else:
            return False

   