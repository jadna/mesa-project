import random
import matplotlib.pyplot as plt
from route import Route
from qlearning import Qlearning


class Model():

    def __init__(self, n_agents, routes):

        self.routes = routes
        self.queue_entry = {}
        self.current_step = 0
        self.volumes = {r.name:[] for r in routes}

        for i in range(n_agents):
            self.queue_entry[i] = self.dispara_agents

        print("Routes:", self.routes)
        print("Queue Entry:", self.queue_entry)
        print("Current Step:", self.current_step)
        print("Volumes:", self.volumes)



    def step(self, action):
        
        if self.current_step in self.queue_entry.keys():
            self.queue_entry[self.current_step](action)

        for route in self.routes:
            route.step(self.current_step)

            self.volumes[route.name].append(route.volume)
        self.current_step += 1
        

    def dispara_agents(self, action):


        route = self.routes[action]
        time_out = route.time_out(self.current_step)
        route.volume += 1
        if time_out in route.queue_exit.keys():
            route.queue_exit[time_out].append((self.current_step, route.release_volume))
        else:
            route.queue_exit[time_out] = [(self.current_step, route.release_volume)]

        print(f"No tempos {self.current_step} adicionou o agente #{self.current_step} na rota {route.name}")

    def get_reward(self):
        
        reward = -sum([route.volume/route.capacity for route in self.routes])
        return reward

def main():
    random.seed(10)

    n_agents = 10
   
    #time_min, volume, capacity
    route1 = Route("route1", 1, 0, 4)
    route2 = Route("route2", 1, 0, 7)
    route3 = Route("route3", 1, 0, 5)

    routes = [route1, route2, route3]

    qlearning = Qlearning(n_agents, len(routes))
    qlearning.initialize_q_table()

    for i in range(qlearning.n_training_episodes):
        print(f"-------------------- start episode {i} -----------------------------")
        qlearning.update_episolon(i)
        model = episode(qlearning, n_agents, routes)
        print(f"-------------------- end   episode {i} -----------------------------")


    for _,v in model.volumes.items():
        plt.plot(range(len(v)), v)
    plt.legend(model.volumes.keys()) 
    plt.show()


def episode(qlearning, n_agents,routes):

    for route in routes:
        route.reset()

    model = Model(n_agents, routes)

    for i in range(100):
        if i < n_agents:
            action = qlearning.epsilon_greedy_policy(i)
        else:
            action = None
        
        model.step(action)

        if i < n_agents-1:
            reward = model.get_reward()
            print(f"I: {i}, Action: {action}, reward: {reward}")
            qlearning.update_qtable(i, action, i+1, reward)

    return model

if __name__ == "__main__":
    main()