import mesa
from model import SystemModel


def agent_portrayal(agent):

    #Função que desenha do tabuleiro dos agentes
    portrayal = {"Shape": "rect", "Filled": "true", "w": 0.5, "h":0.3}
    portrayal["Color"] = "red"
    portrayal["Layer"] = 0

    """if agent.wealth > 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.78"""
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

model_params = {
    "N": mesa.visualization.Slider(
        "Number of vehicles (agents)",
        1,
        1,
        200,
        1,
        description="Choose how many agents to include in the model",
    ),
    "width": 10,
    "height": 10,
}



#Chama a função do model para controlar os agentes
server = mesa.visualization.ModularServer(
    SystemModel, [grid], "Car Model", model_params
)
server.port = 8523

server.launch(open_browser=True)
