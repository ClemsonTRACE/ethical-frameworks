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
    environment='cenv.CustomEnvironment', max_episode_timesteps=20
)

# Create a PPO agent
agent = Agent.create(
    agent='ppo',
    environment=environment,
    # Automatically configured network
    network='auto',
    # PPO optimization parameters
    batch_size=10, update_frequency=2, learning_rate=3e-4, multi_step=10,
    subsampling_fraction=0.33,
    # Reward estimation
    likelihood_ratio_clipping=0.2, discount=0.99, predict_terminal_values=False,
    # Baseline network and optimizer
    baseline=dict(type='auto', size=32, depth=1),
    baseline_optimizer=dict(optimizer='adam', learning_rate=1e-3, multi_step=10),
    # Regularization
    l2_regularization=0.0, entropy_regularization=0.0,
    # Preprocessing
    state_preprocessing='linear_normalization', reward_preprocessing=None,
    # Exploration
    exploration=0.1, variable_noise=0.0,
    # Default additional config values
    config=None,
    parallel_interactions=1,
    # Save agent every 10 updates and keep the 5 most recent checkpoints
    saver=dict(directory='model', frequency=10, max_checkpoints=3),
    # Log all available Tensorboard summaries
    summarizer=dict(directory='summaries', summaries='all'),
    # Do not record agent-environment interaction trace
    recorder=None
)

# Initialize the runner
runner = Runner(agent=agent, environment=environment)

# Start the runner
runner.run(num_episodes=10000)
runner.close()
agent.save(directory='.', format='numpy', append='episodes')

