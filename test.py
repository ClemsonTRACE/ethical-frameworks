from tensorforce.agents import Agent
from tensorforce.environments import Environment
import cenv
from Ethical_Sim import Ethical_Sim

# Create an OpenAI-Gym environment
environment = Environment.create(
    environment='cenv.CustomEnvironment', max_episode_timesteps=25
)

agent = Agent.load(directory='.', format='numpy', environment=environment)

environment.reset()

while True:
    dilemma = environment.getCurrentDilemma()
    input("\n ***Press Enter For Next Dilemma*** \n")
    print(dilemma['Description'])
    actions = agent.act(states=environment.getState())
    choice = int(actions['choice'] > 0.5)
    choice_raw = actions['choice']
    print('\n Option 0: ' + dilemma['Option_0'] + '\n')
    print('\n Option_1: ' + dilemma['Option_1'] + '\n')
    print('\n The AI has chosen option: ' + str(choice))
    print('With a Raw Value of ' + str(choice_raw) + '\n')
    states, terminal, reward = environment.execute(actions=actions)
    agent.observe(terminal=terminal, reward=reward)


#sim.makeNextDilemma(sim.dilemmasDone[-1]["id"],0)
#print(sim.state())
