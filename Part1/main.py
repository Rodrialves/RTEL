import random
import math
import matplotlib.pyplot as plt
import sys
import time as t
import numpy as np

import funtions as f

def main():
    
    # Parameters
    lambda_ = 200
    mu = 1/0.008
    max_capacity = 1# number of channels
    total_calls_target = 10000 # for exponential distribution
    mode = "exp" # "poisson"
    V_min = 1/5 * 1/lambda_ # for ploting the results
    Max = 5 * 1/lambda_ # for ploting the results
    arrival_times = [] 
    max_time = 10000
    delta = 0.001
    blocks=[]
    

    # Run the simulation
    if mode == "exp":
        t0 = t.time_ns()
        data=f.call_network_simulation_exp(lambda_, mu, max_capacity, total_calls_target, arrival_times)
        t1 = t.time_ns()
        #f.plot_results(arrival_times, V_min, Max)
        print(f"\nTime taken to simulate: {(t1 - t0) / 1e9:.3f} seconds")
        print("\nBlocking probability: ", data['Blocking Probability'])
    elif mode == "poisson":
        t0 = t.time_ns()
        data=f.call_network_simulation_poisson(lambda_, mu, max_capacity, max_time, delta, arrival_times)['Blocking Probability']
        blocks.append(data['Blocking Probability'])
        t1 = t.time_ns()
        #f.plot_results(arrival_times, V_min, Max)
        print(f"\nTime taken to simulate: {(t1 - t0) / 1e9:.3f} seconds")
        print("\nBlocking probability: ", data['Blocking Probability'])

if __name__ == '__main__':
    main()