import random
import math
import matplotlib.pyplot as plt
import sys
import time as t
import numpy as np
import pandas as pd
import funtions as f

# Function to run multiple simulations and save results
def run_multiple_simulations(lambda_, mu, max_capacity_list, target_list, mode="exp", delta=None):
    simulation_stats = []

    for max_capacity in max_capacity_list:
        for target in target_list:
            arrival_times = []
            if mode == "exp":
                print(f"\nRunning Exp simulation with max_capacity={max_capacity} and total_calls_target={target}")
                stats = f.call_network_simulation_exp(lambda_, mu, max_capacity, target, arrival_times)
            elif mode == "poisson":
                print(f"\nRunning Poisson simulation with max_capacity={max_capacity} and max_time={target}")
                stats = f.call_network_simulation_poisson(lambda_, mu, max_capacity, target, delta, arrival_times)

            # Save stats and generate unique plot names
            stats['Max Capacity'] = max_capacity
            stats['Target'] = target
            simulation_stats.append(stats)

            # Save plot
            V_min = 1 / 5 * 1 / lambda_
            Max = 5 * 1 / lambda_
            filename = f"plot_{mode}_cap{max_capacity}_target{target}.png"
            f.plot_results(arrival_times, V_min, Max, filename)

    # Save stats to Excel
    df = pd.DataFrame(simulation_stats)
    df.to_excel(f"simulation_results_{mode}.xlsx", index=False)
    print(f"\nResults saved to simulation_results_{mode}.xlsx")

# Main function to run simulations
def main():
    lambda_ = 5
    mu = 0.2
    max_capacity_list = [350]  # Different values of max capacity
    total_calls_target_list_exp = [50, 125, 250, 500, 1250, 2500, 5000, 7500, 10000]  # Total call targets for exponential mode
    max_time_list_poisson = [10, 25, 50, 100, 250, 500, 1000, 1500, 2000]  # Total time for Poisson mode
    delta = 0.001  # Time interval for Poisson mode

    # Run for exponential mode
    run_multiple_simulations(lambda_, mu, max_capacity_list, total_calls_target_list_exp, mode="exp")

    # Run for Poisson mode
    run_multiple_simulations(lambda_, mu, max_capacity_list, max_time_list_poisson, mode="poisson", delta=delta)

if __name__ == '__main__':
    main()
