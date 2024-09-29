import random
import math
import matplotlib.pyplot as plt
import sys

# Define the functions for the simulation

def exponential_time(const):
    return -math.log(1.0 - random.random()) / const

def poisson_time(const):
    return -math.log(1.0 - random.random()) / const

def plot_results(arrival_times, delta, Max):
    # Create the histogram for arrival times
    bins = []
    current_bin = 0

    while current_bin < Max:
        bins.append(current_bin)
        current_bin += delta

    bins.append(Max)  # Ensure the final bin includes values up to Max
    plt.hist(arrival_times, bins=bins, edgecolor='black')
    plt.xlabel('Call Arrival Time Duration')
    plt.ylabel('Number of Occurrences')
    plt.title('Histogram of Call Arrival Times')
    plt.show()

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

        # Check if a new call arrives before any ongoing call ends
            # New call arrives

        if next_call_arrival <= current_time:
            total_calls += 1
            arrival_times.append(call_time)

            if active_calls < max_capacity:
                print(f"Call {total_calls} arrived at {current_time:.2f}.")
                # Accept the call
                call_duration = exponential_time(mu)
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
            call_time = exponential_time(lambda_)
            next_call_arrival = next_call_arrival + call_time

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
    print(f"Average time of arrival between calls: {sum(arrival_times) / total_calls:.2f}")
    print(f"Average number of active calls: {current_time / total_calls:.2f}")
    print(f"Expected number of active calls: {lambda_ / mu:.2f}")
    print(f"Expected call arrival time: {1 / lambda_:.2f}")

def call_network_simulation_poisson(lambda_, mu, max_capacity, total_calls_target, delta, Max):
    print("Running simulation with Poisson call duration.")

def main():

    argv = sys.argv

    if len(argv) != 6:
        print("Usage: python main.py <lambda> <mu> <max_capacity> <total_calls_target> <mode>")
        sys.exit(1)

    # Parameters
    lambda_ = float(argv[1])
    mu = float(argv[2])
    max_capacity = int(argv[3])
    total_calls_target = int(argv[4])
    mode = argv[5]
    delta = 1/5 * 1/lambda_
    Max = 5 * 1/lambda_
    arrival_times = []

    # Run the simulation
    if mode == "exp":
        call_network_simulation_exp(lambda_, mu, max_capacity, total_calls_target, arrival_times)
        plot_results(arrival_times, delta, Max)
        print(f"Times: {arrival_times}")
    elif mode == "poisson":
        call_network_simulation_poisson(lambda_, mu, max_capacity, total_calls_target, delta, Max)

if __name__ == '__main__':
    main()