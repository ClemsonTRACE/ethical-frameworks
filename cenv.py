import os
import logging
import random

import tensorflow as tf

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

from Ethical_Sim import Ethical_Sim

class CustomEnvironment(Environment):
    #sim = Ethical_Sim(20)
    def __init__(self):
        super().__init__() 
    
    def states(self):
        return dict(type='float', shape=(24,))

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

    def getCurrentDilemma(self):
        return self.sim.dilemmasDone[-1]

    def getState(self):
        return self.sim.state()

    def execute(self, actions):
        terminal = False
        #choice selection
        if False: #make true to do over 0.5
            choice = int(actions['choice'] > 0.5)
        else: #make False for pseudo random
            if actions['choice'] > 0.5:
                choice = int(random.uniform(0,1) < actions['choice'])
            else:
                choice = int(random.uniform(0,1) < 1 - actions['choice'])
        #print("choice: " + str(actions['choice']))
        self.sim.makeNextDilemma(self.sim.dilemmasDone[-1]["id"], choice)
        reward = self.sim.reward('util', actions['choice'] > 0.5)
        return self.sim.state(), terminal, reward
