from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random
from agent import Vehicle
from routes import Route

random.seed(10)


class SystemModel(Model):

    def __init__(self, N, width, height, routes_info=0):
        self.num_vehicle = N
        self.routes_info = routes_info
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.max_id = 0
        self.next_creation = random.randint(1, 10) #tempo de criação dos veiculos na fila


        # Criar veículos
        for _ in range(self.num_vehicle):
            self.createVehicle()

    def createVehicle(self):

        vehicle = Vehicle(self.max_id, self, speed=random.randint(1, 10))  # Velocidade aleatória

        self.grid.place_agent(vehicle, (0, 5))
        self.schedule.add(vehicle)
        self.max_id +=1
        
        return vehicle

    def step(self):

        if not self.running: return

        if self.schedule.steps % self.next_creation == 0:
            test = self.createVehicle()
            
            Route.accept_vehicle(self.schedule.agents)

        
        # if self.schedule.steps >= 4:
        #    self.running = False 
        # else:
        self.schedule.step()


