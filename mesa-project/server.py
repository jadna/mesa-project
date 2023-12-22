import mesa
from model import AgentModel
from teste import RouteModel



def agent_portrayal(agent):
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


"""model_params = {
    "num_agents": mesa.visualization.Slider(
        "Number of agents",
        2,
        2,
        200,
        1,
        description="Choose how many agents to include in the model",
    ),
    "width": 10,
    "height": 10,
}"""
model_params = {
    "num_vehicles": mesa.visualization.Slider(
        "Number of agents",
        2,
        2,
        200,
        1,
        description="Choose how many agents to include in the model",
    ),
    "num_requests": mesa.visualization.Slider(
        "Number of requests",
        2,
        2,
        200,
        1,
        description="Choose how many agents to include in the model",
    ),
    "width": 10,
    "height": 10,
}



server = mesa.visualization.ModularServer(
    RouteModel, [grid], "Car Model", model_params
)
server.port = 8522

server.launch(open_browser=True)
