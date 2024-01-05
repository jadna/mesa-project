import mesa


class CarAgent(mesa.Agent):

    def __init__(self, unique_id, model, speed):
        super().__init__(unique_id, model)
        self.speed = speed

    def step(self):
        if self.pos[0] < 5 and self.unique_id == 0:
            self.model.grid.move_agent(self, (self.pos[0]+self.speed, self.pos[1]))
        elif self.unique_id > 0:
            self.model.grid.move_agent(self, (self.pos[0]+self.speed, self.pos[1]))
        

