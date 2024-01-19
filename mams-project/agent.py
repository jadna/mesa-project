from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from model import *
import random


class Agents:
    
    def __init__(self, model):
        
        self.model = model
        self.routes = model.routes

    def dispara_agente(self, action, step):

        route = self.routes[action]
        time_out = route.time_out(step)
        route.volume += 1

        mte = time_out - step #media_time_episodes (mte)
        self.model.times[route.name].append(mte)
        self.model.timeAgents.append(mte)

        if time_out in route.queue_exit.keys():
            route.queue_exit[time_out].append((step, route.release_volume))
        else:
            route.queue_exit[time_out] = [(step, route.release_volume)]

        #print(f"No tempo {step} adicionou o agente #{step} na rota {route.name}")

        return time_out

