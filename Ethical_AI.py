import argparse

args = parser.parse_args()

import os
import logging

import tensorflow as tf

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner
import cenv
from Ethical_Sim import Ethical_Sim

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logger = tf.get_logger()
logger.setLevel(logging.ERROR)

# Create an OpenAI-Gym environment
environment = Environment.create(
    environment='cenv.CustomEnvironment', max_episode_timesteps=10
)

# Create a PPO agent
agent = Agent.create(
    agent='ppo', environment=environment,
    # Automatically configured network
    network='auto',
    # Optimization
    batch_size=10, update_frequency=2, learning_rate=1e-3, subsampling_fraction=0.2,
    optimization_steps=5,
    preprocessing=None,
    # Exploration
    exploration=0.1, variable_noise=0.0,
    # Regularization
    l2_regularization=0.0, entropy_regularization=0.0,
    # TensorFlow etc
    name='agent', device=None, parallel_interactions=1, seed=None, execution=None, saver=None,
    summarizer=None, recorder=None
)
