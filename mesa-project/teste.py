import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Veiculo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.route_choice = random.choice(['Rota1', 'Rota2'])

    def step(self):
        pass

class Rota(Agent):
    def __init__(self, unique_id, model, capacity):
        super().__init__(unique_id, model)
        self.capacity = capacity
        self.veiculos_na_fila = []

    def step(self):
        if len(self.veiculos_na_fila) > 0 and self.capacity > 0:
            veiculo = self.veiculos_na_fila.pop(0)
            self.capacity -= 1
            print(f"Veículo {veiculo.unique_id} escolheu {self.unique_id} e está usando a rota.")
        else:
            print(f"A rota {self.unique_id} está vazia ou atingiu a capacidade máxima.")

class SimulacaoModel(Model):
    def __init__(self, num_veiculos, capacidade_rota):
        self.num_veiculos = num_veiculos
        self.capacidade_rota = capacidade_rota
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(1, 2, True)

        for i in range(self.num_veiculos):
            veiculo = Veiculo(i, self)
            self.schedule.add(veiculo)
            x = random.choice([0, 1])
            self.grid.place_agent(veiculo, (0, x))

        for i in range(2):
            rota = Rota(i+self.num_veiculos, self, self.capacidade_rota)
            self.schedule.add(rota)
            self.grid.place_agent(rota, (0, i))

        self.datacollector = DataCollector()

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

# Parâmetros da simulação
num_veiculos = 10
capacidade_rota = 3
num_steps = 5

# Criar e executar a simulação
simulacao = SimulacaoModel(num_veiculos, capacidade_rota)
for step in range(num_steps):
    print(f"\nPasso de simulação: {step}")
    simulacao.step()