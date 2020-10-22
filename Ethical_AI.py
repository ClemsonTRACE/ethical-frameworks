import argparse

parser = argparse.ArgumentParser()
#parser.add_argument("--theory", help="select an agent type [ppo, vpg, dqn]")
#args = parser.parse_args()

import os
import logging

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner
import cenv
from Ethical_Sim import Ethical_Sim
from tensorforce import Runner

# Create an OpenAI-Gym environment
environment = Environment.create(
    environment='cenv.CustomEnvironment', max_episode_timesteps=25
)

# Create a PPO agent
agent = Agent.create(
    agent='ppo',
    environment=environment,
    # Automatically configured network
    network=[dict(type='dense', size=64),
             dict(type='dense', size=64)],
    # PPO optimization parameters
    batch_size=50, update_frequency=2, learning_rate=3e-4, multi_step=10,
    subsampling_fraction=0.33,
    # Exploration
    exploration=0.3, variable_noise=0.0,
    # Default additional config values
    config=None,
    parallel_interactions=1,
)

# Initialize the runner
runner = Runner(agent=agent, environment=environment)

# Start the runner
runner.run(num_episodes=100000)
runner.close()
agent.save(directory='.', format='numpy', append='episodes')

