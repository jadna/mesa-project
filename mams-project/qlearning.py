import numpy as np
import random


class Qlearning():

    def __init__(self, state_space_size, action_space_size):

        self.state_space_size = state_space_size
        self.action_space_size = action_space_size        
        
        # Training parameters
        self.n_training_episodes = 100
        self.learning_rate = 0.7        

        # Evaluation parameters
        self.n_eval_episodes = 100     

        # Environment parameters
        #self.env_id = "FrozenLake-v1"   
        self.max_steps = 99             
        self.gamma = 0.95               
        self.eval_seed = []             

        # Exploration parameters
        self.max_epsilon = 1.0           
        self.min_epsilon = 0.05           
        self.decay_rate = 0.0005         


    def initialize_q_table(self):
        
        self.Qtable = np.zeros((self.state_space_size, self.action_space_size))
        
    
    def epsilon_greedy_policy(self, state):

        random_int = random.uniform(0,1)
        if random_int > self.epsilon:
            action = np.argmax(self.Qtable[state])
        else:
            action = random.randint(0, self.action_space_size-1)
        return action

    def greedy_policy(self, state):
        action = np.argmax(self.Qtable[state])
        return action
    
    def update_episolon(self, episode):

        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon)*np.exp(-self.decay_rate*episode)
        
    def update_qtable(self, state, action, new_state, reward):
        self.Qtable[state][action] = self.Qtable[state][action] + self.learning_rate * (reward + self.gamma * np.max(self.Qtable[new_state]) - self.Qtable[state][action])
    