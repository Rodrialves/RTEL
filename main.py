import random
import math
import matplotlib.pyplot as plt

def poisson_arrival_time(lambda_):
    return -math.log(1.0 - random.random()) / lambda_

def exponential_duration(mu):
    return -math.log(1.0 - random.random()) / mu

def plot_results(time_data, active_calls_data, total_calls, accepted_calls, dropped_calls, max_capacity, blocking_probability):
    """Plots the results of the simulation."""
    plt.figure(figsize=(12, 6))

    # Plot number of active calls over time
    plt.plot(time_data, active_calls_data, label='Active Calls', color='blue')
    plt.axhline(y=max_capacity, color='red', linestyle='--', label=f'Max Capacity ({max_capacity})')
    plt.xlabel('Time (units)')
    plt.ylabel('Number of Active Calls')
    plt.title(f"Call Traffic Simulation: {total_calls} Total Calls Tried")
    plt.legend()

    # Display statistics as text
    textstr = (f"Total Calls Attempted: {total_calls}\n"
               f"Accepted Calls: {accepted_calls}\n"
               f"Dropped Calls: {dropped_calls}\n"
               f"Blocking Probability: {blocking_probability:.2f}")
    plt.gcf().text(0.15, 0.65, textstr, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

    # Show plot
    plt.show()

def call_network_simulation(lambda_, mu, max_capacity, total_calls_target):
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
    next_call_arrival = poisson_arrival_time(lambda_)
    print(f"First call will arrive at {next_call_arrival:.2f}.")

    while total_calls < total_calls_target:




        # Check if a new call arrives before any ongoing call ends
            # New call arrives

        if next_call_arrival <= current_time:
            total_calls += 1
            if active_calls < max_capacity:
                print(f"Call {total_calls} arrived at {current_time:.2f}.")
                # Accept the call
                call_duration = exponential_duration(mu)
                call_end_time = current_time + call_duration
                events.append(call_end_time)
                active_calls += 1
                accepted_calls += 1
                print(f"Call {total_calls} started at {current_time:.2f} and will end at {call_end_time:.2f}.")
            else:
                print(f"Call {total_calls} arrived at {current_time:.2f}.")
                # Drop the call
                dropped_calls += 1
                print(f"Call {total_calls} dropped at {current_time:.2f}. Capacity full.")
        
            # Schedule next call arrival
            next_call_arrival += poisson_arrival_time(lambda_)

        else:
            if events:
                print(f"Active calls: {active_calls}.")
                # Get the time of the next call ending
                events.sort()
                next_call_end_time = events.pop(0)
                current_time = next_call_end_time
                active_calls -= 1
                print(f"Call ended at {current_time:.2f}. Active calls: {active_calls}.")
            else:
                # If no active calls, just jump to the next arrival time
                current_time = next_call_arrival

        # Track data for plotting
        time_data.append(current_time)
        active_calls_data.append(active_calls)

    # Display final statistics
    print(f"Total calls attempted: {total_calls}")
    print(f"Calls dropped: {dropped_calls}")
    blocking_probability = dropped_calls / total_calls if total_calls > 0 else 0
    print(f"Blocking Probability: {blocking_probability:.2f}") 
    print(f"Average time of arrival between calls: {current_time / total_calls:.2f}")

    # Plot the results
    plot_results(time_data, active_calls_data, total_calls_target, accepted_calls, dropped_calls, max_capacity, blocking_probability)

# Parameters
lambda_ = 0.2
mu = 0.01
max_capacity = 100 
total_calls_target = 10000000

# Run the simulation
call_network_simulation(lambda_, mu, max_capacity, total_calls_target)
