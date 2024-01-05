from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

class Veiculo(Agent):

    def __init__(self, unique_id, model, velocidade):
        super().__init__(unique_id, model)
        self.velocidade = velocidade
        #self.tempo_de_uso = 0
        #self.rota_atual = None

    """def move(self):
        if self.rota_atual:
            next_x, next_y = self.rota_atual.pop(0)
            self.model.grid.move_agent(self, (next_x, next_y))

    def step(self):
        if self.tempo_de_uso > 0:
            self.tempo_de_uso -= 1
        elif self.rota_atual:
            self.move()"""