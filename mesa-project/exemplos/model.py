from typing import Any
from agent import CarAgent
import mesa

class AgentModel(mesa.Model):

    def __init__(self, num_agents=2, width=10, height=10):
        self.num_agents = num_agents
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True


        for i in range(self.num_agents):

            a = CarAgent(i, self, self.random.randrange(4)+1)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = 0
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):

        if not self.running: return
        
        if self.schedule.steps >= 4:
           self.running = False 
        else:
            self.schedule.step()




