######################### ROUTE #########################
# Valores  da BPR retirados da literatura
BETA = 0.15
ALPHA = 4

######################### QLEARNING #########################
N_TRAINING_EPISODES = 10000
LEARNING_RATE = 0.7        

# EVALUATION PARAMETERS
N_EVAL_EPISODES = 100  #Não está sendo usado
EPISODES_LENGTH = 500    

# ENVIRONMENT PARAMETERS
#ENV_ID = "FROZENLAKE-V1"   
MAX_STEPS = 99             
GAMMA = 0.95                         

# EXPLORATION PARAMETERS
MAX_EPSILON = 1.0           
MIN_EPSILON = 0.05           
DECAY_RATE = 0.0005

######################### MODEL #########################
N_AGENTS = 100
TIME_MIN = 0
VOLUME = 0
CAPACITY = 0
SEED = 10
