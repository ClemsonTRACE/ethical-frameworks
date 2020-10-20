import os
import logging

import tensorflow as tf

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

from Ethical_Sim import Ethical_Sim

class CustomEnvironment(Environment):
    sim = Ethical_Sim(20)
    def __init__(self):
        super().__init__() 
    
    def states(self):
        return dict(type='float', shape=(38,))

    def actions(self):
        return {"choice": dict(type="float", min_value=0.0, max_value=1.0)}

    # Optional, should only be defined if environment has a natural maximum
    # episode length
    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    # Optional
    def close(self):
        super().close()

    def reset(self):
        self.sim = Ethical_Sim(20)
        return self.sim.state()

    def execute(self, actions):
        terminal = False
        self.sim.makeNextDilemma(self.sim.dilemmasDone[-1]["id"],int(actions['choice'] > 0.5))
        reward = self.sim.reward('util', actions['choice'] > 0.5)
        return self.sim.state(), terminal, reward
