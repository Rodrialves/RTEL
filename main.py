import random
import math
import matplotlib.pyplot as plt
import sys
import time as t
import numpy as np

import funtions as f

def main():

    argv = sys.argv

    if len(argv) != 6 and len(argv) != 7:
        print("Usage: python main.py <lambda> <mu> <max_capacity> <total_calls_target / sim_time> <mode> (<delta>)")
        sys.exit(1)
    # Parameters
    lambda_ = float(argv[1])
    mu = float(argv[2])
    max_capacity = int(argv[3])
    total_calls_target = int(argv[4])
    mode = argv[5]
    V_min = 1/5 * 1/lambda_
    Max = 5 * 1/lambda_
    arrival_times = []
    max_time = float(argv[4])
    if mode == "poisson":
        delta = float(argv[6])
        
    # Run the simulation
    if mode == "exp":
        t0 = t.time_ns()
        f.call_network_simulation_exp(lambda_, mu, max_capacity, total_calls_target, arrival_times)
        t1 = t.time_ns()
        f.plot_results(arrival_times, V_min, Max)
        print(f"\nTime taken to simulate: {(t1 - t0) / 1e9:.3f} seconds")
    elif mode == "poisson":
        t0 = t.time_ns()
        f.call_network_simulation_poisson(lambda_, mu, max_capacity, max_time, delta, arrival_times)
        t1 = t.time_ns()
        f.plot_results(arrival_times, V_min, Max)
        print(f"\nTime taken to simulate: {(t1 - t0) / 1e9:.3f} seconds")

if __name__ == '__main__':
    main()