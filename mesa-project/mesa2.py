from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

class Veiculo(Agent):
    def __init__(self, unique_id, model, velocidade):
        super().__init__(unique_id, model)
        self.velocidade = velocidade
        self.tempo_de_uso = 0
        self.rota_atual = None

    def move(self):
        if self.rota_atual:
            next_x, next_y = self.rota_atual.pop(0)
            self.model.grid.move_agent(self, (next_x, next_y))

    def step(self):
        if self.tempo_de_uso > 0:
            self.tempo_de_uso -= 1
        elif self.rota_atual:
            self.move()

class Rota(Agent):
    def __init__(self, unique_id, model, capacidade, comprimento):
        super().__init__(unique_id, model)
        self.capacidade = capacidade
        self.veiculos_na_fila = []
        self.comprimento = comprimento

    def aceitar_veiculo(self, veiculo):
        if len(self.veiculos_na_fila) < self.capacidade:
            self.veiculos_na_fila.append(veiculo)
            veiculo.rota_atual = self.gerar_caminho()
            return True
        else:
            return False

    def calcular_tempo_de_uso(self, veiculo):
        fator_veiculos = len(self.veiculos_na_fila) / self.capacidade
        return (self.comprimento / veiculo.velocidade) * (1 + fator_veiculos)

    def gerar_caminho(self):
        # Gera um caminho aleatório dentro da rota
        x, y = self.pos
        caminho = [(x, y)]
        for _ in range(self.comprimento - 1):
            neighbors = self.model.grid.get_neighborhood((x, y), moore=True, include_center=False)
            next_x, next_y = random.choice(neighbors)
            caminho.append((next_x, next_y))
            x, y = next_x, next_y
        return caminho

class SistemaModel(Model):
    def __init__(self, N, rotas_info):
        self.num_veiculos = N
        self.rotas_info = rotas_info
        self.grid = MultiGrid(10, 10, True)
        self.schedule = RandomActivation(self)

        # Criar veículos
        for i in range(self.num_veiculos):
            veiculo = Veiculo(i, self, velocidade=random.uniform(1, 5))  # Velocidade aleatória
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(veiculo, (x, y))
            self.schedule.add(veiculo)

        # Criar rotas
        for i, (capacidade, comprimento) in enumerate(self.rotas_info):
            rota = Rota(i+self.num_veiculos, self, capacidade, comprimento)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(rota, (x, y))
            self.schedule.add(rota)

        self.datacollector = DataCollector(
            agent_reporters={"Posição": "pos", "Tempo de Uso": "tempo_de_uso", "Velocidade": "velocidade"}
        )

    def associar_veiculos_rotas(self):
        veiculos = [agente for agente in self.schedule.agents if isinstance(agente, Veiculo)]
        rotas = [agente for agente in self.schedule.agents if isinstance(agente, Rota)]

        for veiculo in veiculos:
            rota_disponivel = random.choice(rotas)
            if rota_disponivel.aceitar_veiculo(veiculo):
                # veiculo.rota_atual = rota_disponivel.gerar_caminho() # Não necessário, pois o veículo só se move quando o tempo de uso é 0
                pass

    def step(self):
        self.associar_veiculos_rotas()
        self.datacollector.collect(self)
        self.schedule.step()

# Exemplo de uso
rotas_info = [(3, 5), (2, 8)]  # (capacidade, comprimento)
modelo = SistemaModel(N=5, rotas_info=rotas_info)

# Executar por 100 passos de simulação
for i in range(100):
    modelo.step()

# Obter dados para análise
dados = modelo.datacollector.get_agent_vars_dataframe().groupby('Step').agg({
    'Posição': 'unique',
    'Tempo de Uso': 'sum',
    'Velocidade': 'mean'
})
print(dados)
