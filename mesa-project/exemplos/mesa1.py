from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

class Veiculo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)

class Rota(Agent):
    def __init__(self, unique_id, model, capacidade):
        super().__init__(unique_id, model)
        self.capacidade = capacidade
        self.veiculos_na_fila = []

    def aceitar_veiculo(self, veiculo):
        if len(self.veiculos_na_fila) < self.capacidade:
            self.veiculos_na_fila.append(veiculo)
            return True
        else:
            return False

class SistemaModel(Model):
    def __init__(self, N, M):
        self.num_veiculos = N
        self.num_rotas = M
        self.grid = MultiGrid(10, 10, True)
        self.schedule = RandomActivation(self)

        # Criar veículos
        for i in range(self.num_veiculos):
            veiculo = Veiculo(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(veiculo, (x, y))
            self.schedule.add(veiculo)

        # Criar rotas
        for i in range(self.num_rotas):
            capacidade = random.randint(1, 3)  # Capacidade máxima de veículos na rota
            rota = Rota(i, self, capacidade)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(rota, (x, y))
            self.schedule.add(rota)

        self.datacollector = DataCollector(
            agent_reporters={"Posição": "pos"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Criar instância do modelo
modelo = SistemaModel(N=5, M=2)

# Executar por 100 passos de simulação
for i in range(100):
    modelo.step()

# Obter dados para análise
dados = modelo.datacollector.get_agent_vars_dataframe().groupby('Step').Posição.unique()
print(dados)
