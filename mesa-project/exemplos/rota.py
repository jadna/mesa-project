from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import networkx as nx
import matplotlib.pyplot as plt

class VehicleAgent(Agent):
    def __init__(self, unique_id, model, path):
        super().__init__(unique_id, model)
        self.path = path  # Caminho pré-definido
        self.current_position = self.path[0]

    def move_along_path(self):
        if len(self.path) > 1:
            self.current_position = self.path.pop(0)

    def step(self):
        self.move_along_path()

class RoadNetworkModel(Model):
    def __init__(self, road_graph, num_vehicles):
        self.num_vehicles = num_vehicles
        self.grid = MultiGrid(len(road_graph.nodes), 1, False)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector()

        # Create vehicles
        for i in range(self.num_vehicles):
            path = list(road_graph.nodes)
            agent = VehicleAgent(i, self, path=path)
            x, y = agent.current_position
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        self.road_graph = road_graph

    def step(self):
        # Move vehicles along their predefined paths
        self.schedule.step()
        self.datacollector.collect(self)

def visualize_network_and_agents(road_graph, model):
    pos = {node: (node[1], -node[0]) for node in road_graph.nodes}  # Flip y-axis for better visualization
    nx.draw(road_graph, pos=pos, with_labels=True, node_size=100, font_size=8, font_color='white')
    agent_positions = {agent.unique_id: agent.current_position for agent in model.schedule.agents}
    nx.draw_networkx_nodes(road_graph, pos=agent_positions, node_size=50, node_color='red', label='Vehicles')
    plt.show()

# Create a simple road network using networkx
G = nx.grid_2d_graph(5, 1)

# Specify edges as roads
roads = [((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)), ((3, 0), (4, 0))]
G.remove_edges_from(list(G.edges))
G.add_edges_from(roads)

# Set up the model with the road network and run the simulation
num_vehicles = 5

model = RoadNetworkModel(G, num_vehicles)

# Visualize the road network and initial positions of vehicles
visualize_network_and_agents(G, model)

# Run the simulation for some steps
for i in range(5):
    model.step()

# Visualize the road network and final positions of vehicles
visualize_network_and_agents(G, model)
    