import random
from route import Route
import matplotlib.pyplot as plt

class Model():

    def __init__(self, n_agents, routes):

        self.routes = routes
        self.queue_entry = {}
        self.current_step = 0
        self.volumes = {r.name:[] for r in routes}

        for i in range(n_agents):
            self.queue_entry[i] = self.dispara_agents



    def step(self):
        
        if self.current_step in self.queue_entry.keys():
            self.queue_entry[self.current_step]()

        for route in self.routes:
            route.step(self.current_step)

            self.volumes[route.name].append(route.volume)
        self.current_step += 1
        

    def dispara_agents(self):

        #Aqui é a rota
        route = self.routes[random.randint(0, len(self.routes)-1)]
        time_out = route.time_out(self.current_step)
        route.volume += 1
        if time_out in route.queue_exit.keys():
            route.queue_exit[time_out].append(route.release_volume)
        else:
            route.queue_exit[time_out] = [route.release_volume]

        print(f"No tempos {self.current_step} adicionou um agente na rota {route.name}")

        

def main():

    random.seed(1)
    #time_min, volume, capacity
    route1 = Route("route1", 1, 0, 4)
    route2 = Route("route2", 1, 1, 7)
    route3 = Route("route3", 1, 3, 5)
    
    model = Model(10, [route1, route2, route3])

    for _ in range(100):
        model.step()

    for _,v in model.volumes.items():
        plt.plot(range(len(v)), v)
    plt.legend(model.volumes.keys()) 
    plt.show()

if __name__ == "__main__":
    main()