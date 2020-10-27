#Test file for the AI agents trained.
#This file does not automate training but rather graphically
#displays agent choices for human interpretation. 

#Tensorforce Requirements
from tensorforce.agents import Agent
from tensorforce.environments import Environment

#Custom File Requirements
import cenv
from Ethical_Sim import Ethical_Sim

# Create an OpenAI-Gym environment
environment = Environment.create(
    environment='cenv.CustomEnvironment', max_episode_timesteps=25
)

#Load the Agent Previously Saved
agent = Agent.load(directory='.', format='numpy', environment=environment)

#Set up the Environment
environment.reset()

while True:
    #Get the Current Dilemma for Output and wait for human input
    dilemma = environment.getCurrentDilemma()
    input("\n ***Press Enter For Next Dilemma*** \n")
    
    #Have the AI Generate Actions based on Current Dilemma
    actions = agent.act(states=environment.getState())

    #Output printing for human verification
    choice = int(actions['choice'] > 0.5)
    choice_raw = actions['choice']
    print(dilemma['Description'])
    print('\n Option 0: ' + dilemma['Option_0'])
    util_r = str(environment.getReward('util', 0))
    deon_r = str(environment.getReward('deon', 0))
    virt_r = str(environment.getReward('virtue', 0))
    print(" -- Util Reward: " + util_r + "" + " -- Deon Reward: " + deon_r + " -- Virtue Reward: " + virt_r + '\n')
    print('\n Option_1: ' + dilemma['Option_1'] + '\n')
    util_r = str(environment.getReward('util', 1))
    deon_r = str(environment.getReward('deon', 1))
    virt_r = str(environment.getReward('virtue', 1))
    print(" -- Util Reward: " + util_r + "" + " -- Deon Reward: " + deon_r + " -- Virtue Reward: " + virt_r + '\n') 
    print('\n The AI has chosen option: ' + str(choice))
    print('With a Raw Value of ' + str(choice_raw) + '\n')

    #Excecute the Action taken, may need to modify for Production
    states, terminal, reward = environment.execute(actions=actions)

    #Give reward to agent, needed to do another action
    agent.observe(terminal=terminal, reward=reward)


