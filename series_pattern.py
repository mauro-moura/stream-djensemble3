import numpy as np
from random import random

def add_noise_decorator(function):
    def inner1(num_time_steps):
        return function(num_time_steps) + [random() * 3 for _ in range(num_time_steps)]
    return inner1

# Functions to generate different patterns
# 1: 'linear'
@add_noise_decorator
def generate_linear(num_time_steps):
    if num_time_steps < 100:
        return np.linspace(0, 100, num_time_steps)
    if num_time_steps < 1000:
        return np.linspace(0, 1000, num_time_steps)
    elif num_time_steps < 10000:
        return np.linspace(0, 10000, num_time_steps)
    else:
        return np.linspace(0, num_time_steps*10, num_time_steps)

# 2: 'sinusoidal'
@add_noise_decorator    
def generate_sinusoidal(num_time_steps):
    return 5 * np.sin(np.linspace(0, 10, num_time_steps))

# 3: 'random_walk'
@add_noise_decorator
def generate_random_walk(num_time_steps):
    return np.cumsum(np.random.randn(num_time_steps))

# 4: 'exponential'
@add_noise_decorator
def generate_exponential_growth(num_time_steps):
    growth_rate=1.05
    return growth_rate ** np.arange(num_time_steps) + np.random.randn(1, num_time_steps)

class SeriesPattern():
    def __init__(self, pattern_name):
        if pattern_name == "linear":
            self.key = 1
            self.function = generate_linear
            self.name = pattern_name            
        elif pattern_name == "sinusoidal":
            self.key = 2
            self.function = generate_sinusoidal
            self.name = pattern_name
        elif pattern_name == "random_walk":
            self.key = 3
            self.function = generate_random_walk
            self.name = pattern_name
        elif pattern_name == "exponential_growth":
            self.key = 4
            self.function = generate_exponential_growth
            self.name = pattern_name