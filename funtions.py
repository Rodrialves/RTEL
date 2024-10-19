import random
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import pandas as pd

def exponential_time(const):
    return -math.log(1.0 - random.random()) / const

def poisson_time(delta,const):
    rand_val = random.random()
    decision = delta * const

    if rand_val < decision:
        return True
    else:
        return False
    
def plot_results(arrival_times, delta, Max, filename=None):
    bins = []
    current_bin = 0

    while current_bin < Max:
        bins.append(current_bin)
        current_bin += delta

    bins.append(Max)  # Ensure the final bin includes values up to Max
    plt.hist(arrival_times, bins=bins, edgecolor='black', alpha=0.6, color='g')

    # Plot the exponential distribution
    lambda_ = 1 / (sum(arrival_times) / len(arrival_times))  # Estimate lambda from the data
    x = np.linspace(0, Max, 1000)
    y = len(arrival_times) * lambda_ * np.exp(-lambda_ * x) * delta  # Scale the y-values to match the histogram
    plt.plot(x, y, 'r-', lw=2, label='Exponential Distribution')

    plt.xlabel('Call Arrival Time')
    plt.ylabel('Number of Calls')
    plt.title('Histogram of Call Arrival Times')
    plt.legend()

    if(filename == None): # Show the plot if no filename is given
        plt.show()
    else: # Save the plot before showing it
        plt.savefig(filename)
        plt.close()
        
def call_network_simulation_exp(lambda_, mu, max_capacity, total_calls_target, arrival_times):

    print("Running simulation with exponential call duration.")
    current_time = 0
    active_calls = int(random.random() * max_capacity)  # Number of currently active calls
    total_calls = 0  # Total number of call attempts
    dropped_calls = 0  # Track dropped calls
    events = []  # List of active call events (start, end times)
    
    # To track data for plotting
    time_data = []  # Track current time
    active_calls_data = []  # Number of active calls over time
    accepted_calls = 0  # Calls that were accepted and not dropped

    # Generate initial call arrival time
    call_time = exponential_time(lambda_)
    next_call_arrival = call_time
    print(f"First call will arrive at {next_call_arrival:.2f}.")

    while total_calls < total_calls_target:
        if next_call_arrival <= current_time:
            total_calls += 1
            arrival_times.append(call_time)

            if active_calls < max_capacity:
                print(f"Call {total_calls} arrived at {current_time:.2f}.")
                call_duration = exponential_time(mu)
                call_end_time = current_time + call_duration
                events.append(call_end_time)
                active_calls += 1
                accepted_calls += 1
                print(f"Call {total_calls} started at {current_time:.2f} and will end at {call_end_time:.2f}.")
            else:
                print(f"Call {total_calls} arrived at {current_time:.2f}.")
                dropped_calls += 1
                print(f"Call {total_calls} dropped at {current_time:.2f}. Capacity full.")
        
            call_time = exponential_time(lambda_)
            next_call_arrival = next_call_arrival + call_time

        else:
            if events:
                print(f"Active calls: {active_calls}.")
                events.sort()
                next_call_end_time = events.pop(0)
                current_time = next_call_end_time
                active_calls -= 1
                print(f"Call ended at {current_time:.2f}. Active calls: {active_calls}.")
            else:
                current_time = next_call_arrival

        time_data.append(current_time)
        active_calls_data.append(active_calls)

    blocking_probability = dropped_calls / total_calls if total_calls > 0 else 0

    return {
        'Total Calls': total_calls,
        'Dropped Calls': dropped_calls,
        'Blocking Probability': blocking_probability,
        'Average Arrival Time': sum(arrival_times) / total_calls if total_calls > 0 else 0,
    }

def call_network_simulation_poisson(lambda_, mu, max_capacity, max_time, delta, arrival_times):
    print("Running simulation with Poisson call duration.")
    current_time = 0
    active_calls = int(random.random() * max_capacity)  # Number of currently active calls
    total_calls = 0  # Total number of call attempts
    dropped_calls = 0  # Track dropped calls
    events = []  # List of active call events (start, end times)
    
    # Generate initial call arrival time
    current_time = delta
    call_time = current_time
    next_call_end_time = 0
    print(f"First call will arrive at {call_time:.2f}.")

    while current_time < max_time:
        if poisson_time(delta,lambda_):
            total_calls += 1
            arrival_times.append(call_time)

            if active_calls < max_capacity:
                print(f"Call {total_calls} arrived at {current_time:.2f}.")
                call_duration = exponential_time(mu)
                call_end_time = current_time + call_duration
                events.append(call_end_time)
                active_calls += 1
            else:
                print(f"Call {total_calls} dropped at {current_time:.2f}. Capacity full.")
                dropped_calls += 1

            call_time = 0
        else:
            if events:
                if next_call_end_time < current_time:
                    events.sort()
                    next_call_end_time = events.pop(0)
                    active_calls -= 1

        current_time += delta
        call_time += delta

    blocking_probability = dropped_calls / total_calls if total_calls > 0 else 0

    return {
        'Total Calls': total_calls,
        'Dropped Calls': dropped_calls,
        'Blocking Probability': blocking_probability,
        'Average Arrival Time': sum(arrival_times) / total_calls if total_calls > 0 else 0,
    }
    
# Function to run multiple simulations and save results
def run_multiple_simulations(lambda_, mu, max_capacity_list, target_list, mode="exp", delta=None):
    simulation_stats = []

    for max_capacity in max_capacity_list:
        for target in target_list:
            arrival_times = []
            if mode == "exp":
                print(f"\nRunning Exp simulation with max_capacity={max_capacity} and total_calls_target={target}")
                stats = call_network_simulation_exp(lambda_, mu, max_capacity, target, arrival_times)
            elif mode == "poisson":
                print(f"\nRunning Poisson simulation with max_capacity={max_capacity} and max_time={target}")
                stats = call_network_simulation_poisson(lambda_, mu, max_capacity, target, delta, arrival_times)

            # Save stats and generate unique plot names
            stats['Max Capacity'] = max_capacity
            stats['Target'] = target
            simulation_stats.append(stats)

            # Save plot
            V_min = 1 / 5 * 1 / lambda_
            Max = 5 * 1 / lambda_
            filename = f"plot_{mode}_cap{max_capacity}_target{target}.png"
            plot_results(arrival_times, V_min, Max, filename)

    # Save stats to Excel
    df = pd.DataFrame(simulation_stats)
    df.to_excel(f"simulation_results_{mode}.xlsx", index=False)
    print(f"\nResults saved to simulation_results_{mode}.xlsx")