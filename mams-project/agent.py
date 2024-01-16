from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from model import *
import random


class Agents:
    
    def __init__(self, model):

        self.routes = model.routes
        self.current_step = 0

    def dispara_agente(self, action):
        # Escolha aleatória de uma rota
        #action = random.choice(list(self.routes.keys()))

        route = self.routes[action]
        time_out = route.time_out(self.current_step)
        route.volume += 1

        if time_out in route.queue_exit.keys():
            route.queue_exit[time_out].append((self.current_step, route.release_volume))
        else:
            route.queue_exit[time_out] = [(self.current_step, route.release_volume)]

        print(f"No tempo {self.current_step} adicionou o agente #{self.current_step} na rota {route.name}")

