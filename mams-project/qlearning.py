import numpy as np
import pandas as pd
import random
from configuration import *

class Qlearning():

    def __init__(self, state_space_size, action_space_size):

        self.state_space_size = state_space_size
        self.action_space_size = action_space_size        
        
        # Training parameters
        self.n_training_episodes = N_TRAINING_EPISODES
        self.learning_rate = LEARNING_RATE      

        # Evaluation parameters
        #self.n_eval_episodes = N_EVAL_EPISODES     

        # Environment parameters
        #self.env_id = "FrozenLake-v1"   
        self.max_steps = MAX_STEPS             
        self.gamma = GAMMA               
        self.eval_seed = []             

        # Exploration parameters
        self.max_epsilon = MAX_EPSILON           
        self.min_epsilon = MIN_EPSILON         
        self.decay_rate = DECAY_RATE        


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
    
        df = pd.DataFrame(self.Qtable)
        df["route"] = df.apply(np.argmax, axis=1)
        df.to_csv('./data/qlearning.csv', index=False)
    