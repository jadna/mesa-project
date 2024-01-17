import random
import matplotlib.pyplot as plt
import pandas as pd
from route import Route
from qlearning import Qlearning
from configuration import *
from agent import *
import numpy as np


class Model():

    def __init__(self, n_agents, routes):

        self.routes = routes
        self.queue_entry = {}
        self.current_step = 0
        self.volumes = {r.name:[] for r in routes}

        for i in range(n_agents):
            #self.queue_entry[i] = self.dispara_agents
            agente = Agents(self)
            self.queue_entry[i] = agente.dispara_agente

        #print("Routes:", self.routes)
        #print("Queue Entry:", self.queue_entry)
        #print("Current Step:", self.current_step)
        #print("Volumes:", self.volumes)

    def step(self, action):
        time_out = None
        if self.current_step in self.queue_entry.keys():
            time_out = self.queue_entry[self.current_step](action, self.current_step)

        for route in self.routes:
            route.step(self.current_step)

            self.volumes[route.name].append(route.volume)
        self.current_step += 1
        return time_out
        

    """def dispara_agents(self, action):


        route = self.routes[action]
        time_out = route.time_out(self.current_step)
        route.volume += 1
        if time_out in route.queue_exit.keys():
            route.queue_exit[time_out].append((self.current_step, route.release_volume))
        else:
            route.queue_exit[time_out] = [(self.current_step, route.release_volume)]

        print(f"No tempos {self.current_step} adicionou o agente #{self.current_step} na rota {route.name}")"""

    def get_reward(self, time_out):

        #reward = -sum([route.volume/route.capacity for route in self.routes])
        #reward = 999999-sum([route.volume/route.capacity for route in self.routes])
        reward = 1/time_out
        return reward

def main():
    #random.seed(SEED)

    n_agents = N_AGENTS

    routesDF = pd.read_csv('./data/routes.csv')
    routes = []

    for _, route in routesDF.iterrows():
        routes.append(Route(route["route_name"], route["time_min"], route["volume"], route["capacity"]))

    qlearning = Qlearning(n_agents, len(routes))
    qlearning.initialize_q_table()
    epsilons = []

    rewards = np.zeros((n_agents,1))
    rewards_sum = []

    for i in range(qlearning.n_training_episodes):
        print(f"-------------------- start episode {i} -----------------------------")
        qlearning.update_episolon(i)
        epsilons.append(qlearning.epsilon)
        model = episode(qlearning, n_agents, routes)
        print(f"--------------------- end episode {i} ------------------------------")

        #Rewards pelo quantidade de episodios
        rwrds = np.array([[max(row)] for row in qlearning.Qtable])
        rewards = np.hstack((rewards, rwrds))
        # UM rewards
        rwrds_sum = sum(np.array([[max(row)] for row in qlearning.Qtable]))
        rewards_sum.append(rwrds_sum)
        
    df = pd.DataFrame(rewards)
    df.to_csv('./data/rewards.csv', index=False)
    #return

    #plot volume das rotas
    for _,v in model.volumes.items():
        plt.plot(range(len(v)), v)
    plt.legend(model.volumes.keys()) 
    plt.show()

    #plot epsilos
    plt.plot(range(len(epsilons)), epsilons)
    plt.show()

    #rewards
    plt.plot(rewards.T)
    plt.show()

    #Soma dos rewards
    plt.plot(range(len(rewards_sum)), rewards_sum)
    plt.show()


def episode(qlearning, n_agents,routes):

    for route in routes:
        route.reset()

    model = Model(n_agents, routes)

    for i in range(EPISODES_LENGTH):
        if i < n_agents:
            action = qlearning.epsilon_greedy_policy(i)
        else:
            action = None
        
        time_out = model.step(action)

        if i < n_agents-1 and time_out != None:
            reward = model.get_reward(time_out)
            print(f"I: {i}, Action: {action}, reward: {reward}")
            qlearning.update_qtable(i, action, i+1, reward)



    if qlearning.epsilon == MIN_EPSILON:
        print(f"Epsilon atingiu o minimo: {qlearning.epsilon}")

    print(f"Epsilon: {qlearning.epsilon}")


    return model

if __name__ == "__main__":
    main()