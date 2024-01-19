import random
import matplotlib.pyplot as plt
import pandas as pd
from route import Route
from qlearning import Qlearning
from configuration import *
from agent import *
import numpy as np
from time import time

class Model():

    def __init__(self, n_agents, routes):

        self.routes = routes
        self.queue_entry = {}
        self.current_step = 0
        self.volumes = {r.name:[] for r in routes}
        self.times = {r.name:[] for r in routes}

        for i in range(n_agents):
            #self.queue_entry[i] = self.dispara_agents
            agente = Agents(self)
            self.queue_entry[i] = agente.dispara_agente

        ##print("Routes:", self.routes)
        ##print("Queue Entry:", self.queue_entry)
        ##print("Current Step:", self.current_step)
        ##print("Volumes:", self.volumes)

    def step(self, action):
        time_out = None
        if self.current_step in self.queue_entry.keys():
            time_out = self.queue_entry[self.current_step](action, self.current_step)

        for route in self.routes:
            route.step(self.current_step)

            self.volumes[route.name].append(route.volume)
        self.current_step += 1
        return time_out
        

    def get_reward(self, time_out):

        #reward = -sum([route.volume/route.capacity for route in self.routes])
        #reward = 999999-sum([route.volume/route.capacity for route in self.routes])
        reward = 1/time_out
        return reward

def main(n_agents):
    #random.seed(SEED)
    for scenario in SCENARIOS:

        routesDF = pd.read_csv('./data/'+str(scenario)+'/routes.csv')
        routes = []

        for _, route in routesDF.iterrows():
            routes.append(Route(route["route_name"], route["time_min"], route["volume"], route["capacity"]))

        qlearning = Qlearning(n_agents, len(routes))
        qlearning.initialize_q_table()
        epsilons = []

        rewards = np.zeros((n_agents,1))
        rewards_sum = []

        timesMeans = {r.name:[] for r in routes}

        for i in range(qlearning.n_training_episodes):
            startT = time()
            ##print(f"-------------------- start episode {i} -----------------------------")
            qlearning.update_episolon(i)
            epsilons.append(qlearning.epsilon)
            model = episode(qlearning, n_agents, routes, scenario)
            deltaT = time() - startT
            expectedT = (qlearning.n_training_episodes - i)*deltaT
            #print(f"--------------------- end episode {i} ------------------------------")
            print(f"{scenario} with {n_agents} agents - {round((i+1)*100/qlearning.n_training_episodes,2)}% - Finished episode {i} in {round(deltaT,2)}seconds, remaining time: {round(expectedT/60,2)} minutes")

            #Rewards pelo quantidade de episodios
            rwrds = np.array([[max(row)] for row in qlearning.Qtable])
            rewards = np.hstack((rewards, rwrds))
            # UM rewards
            rwrds_sum = sum(np.array([[max(row)] for row in qlearning.Qtable]))
            rewards_sum.append(rwrds_sum)

            # Mean time for episodes
            for routeName, timesList in model.times.items():
                mean = sum(timesList)/len(timesList)
                timesMeans[routeName].append(mean)
 
        df = pd.DataFrame(rewards)
        df.to_csv('./data/'+str(scenario)+'/rewards_'+str(n_agents)+'_agents.csv', index=False)

        #plot volume of routes
        for _,v in model.volumes.items():
            plt.plot(range(len(v)), v)
        plt.legend(model.volumes.keys()) 
        plt.title("Volume of Routes "+str(n_agents)+" Agents") 
        plt.xlabel("Time")
        plt.ylabel("Number of agents on the route")
        plt.savefig('./data/'+str(scenario)+'/volume_'+str(n_agents)+'_agents.png')
        plt.clf()
        
        #plot epsilons
        plt.plot(range(len(epsilons)), epsilons)
        plt.title("Epsilon "+str(n_agents)+" Agents") 
        plt.xlabel("Episodes")
        plt.ylabel("Epsilon")
        plt.savefig('./data/'+str(scenario)+'/epsilon_'+str(n_agents)+'_agents.png')
        plt.clf()
        
        #rewards
        plt.plot(rewards.T)
        plt.title("Rewards "+str(n_agents)+" Agents")
        plt.xlabel("Episodes")
        plt.ylabel("Rewards")
        plt.savefig('./data/'+str(scenario)+'/rewards_'+str(n_agents)+'_agents.png')
        plt.clf()
        
        #Sum of rewards
        plt.plot(range(len(rewards_sum)), rewards_sum)
        plt.title("Sum Rewards "+str(n_agents)+" Agents") 
        plt.xlabel("Episodes")
        plt.ylabel("Sum of Rewards")
        plt.savefig('./data/'+str(scenario)+'/sum_rewards_'+str(n_agents)+'_agents.png')
        plt.clf()

        # Mean for time for episodes
        for routeName, means in timesMeans.items(): 
            plt.plot(range(len(means)), means)
        plt.title("Mean Time per Episode by Routes "+str(n_agents)+" Agents") 
        plt.xlabel("Episodes")
        plt.ylabel("Mean Time")
        plt.savefig('./data/'+str(scenario)+'/mean_time_episodes_'+str(n_agents)+'_agents.png')
        plt.legend(timesMeans.keys())
        plt.show()
    

def episode(qlearning, n_agents,routes, scenario):

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
            #print(f"I: {i}, Action: {action}, reward: {reward}")
            qlearning.update_qtable(i, action, i+1, reward, scenario, n_agents)

    return model

if __name__ == "__main__":

    for i in N_AGENTS:
        main(i)