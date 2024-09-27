import numpy as np

import matplotlib.pyplot as plt

LAMBDA = 0.2
MU = 0.5
MAX_CAPACITY = 500
N_SAMPLES = 1000

def generate_random():
    return np.random.rand(100)

def call_arrival(lambda1):
    return np.random.exponential(1/lambda1)

def add_to_plot(x, y):


def main():
    total_call = 0
    calls_dropped = 0



if __name__ == "__main__":
    main()