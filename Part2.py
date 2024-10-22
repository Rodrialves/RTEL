import random
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class Event:
    event_type : str
    time : float

def exponential_time(const):
    return -math.log(1.0 - random.random()) / const

def poisson_time(delta,const):
    rand_val = random.random()
    decision = delta * const

    if rand_val < decision:
        return True
    else:
        return False


def simulation(lambda_, mu, channels, simulation_calls, queue_length, delayed_intervals, max_delay=0.5):
    """
    This function simulates a call center using a queueing model.
    Parameters:
    - lambda_ (float): Arrival rate (calls per time unit).
    - mu (float): Service rate (calls handled per time unit).
    - channels (int): Number of channels in the system.
    - simulation_calls (int): Number of calls to simulate.
    - queue_length (int): Length of the queue. Use 0 for Erlang-B, -1 for Erlang-C, and any other integer for a general case.
    - delayed_intervals (list): List to store the delay intervals for delayed calls.
    - max_delay (float, optional): Maximum delay to consider for service level calculation. Default is 0.5.
    Returns:
    - For Erlang-B:
        - blocking_prob (float): Probability that a call is blocked.
    - For Erlang-C:
        - delayed_prob (float): Probability that a call is delayed.
        - average_delay (float): Average delay of delayed calls.
        - prob_over_Am (float): Probability that the delay is less than max_delay.
    """
    # Initialize the simulation
    time = 0
    events = []
    
    channels_occupied = 0
    blocked_calls = 0
    
    waiting_queue = []
    delayed_calls = 0
    
    total_calls = 0

    # Generate first call
    events.append(Event("arrival", exponential_time(lambda_)))
    total_calls += 1

    # Start simulation
    while total_calls < simulation_calls:
        # Get the next event
        events.sort(key=lambda events: events.time) #sort events by time
        event = events.pop(0) 
        time = event.time #update time
                
        # Process the event
        if event.event_type == "arrival":
            # Generate next arrival event
            events.append(Event("arrival", time + exponential_time(lambda_)))
            total_calls += 1

            # If there are free channels, start service
            if channels_occupied < channels:
                channels_occupied += 1
                events.append(Event("departure", time + exponential_time(mu)))
            # Otherwise, increment blocking calls
            elif((queue_length > 0 and len(waiting_queue) < queue_length) or queue_length==-1): #if the queue is not full, add the call to the queue
                waiting_queue.append(event)
                delayed_calls += 1
            else: #if the queue is full, increment the number of blocked calls
                blocked_calls += 1
                
        elif event.event_type == "departure":
            
            events.sort(key=lambda events: events.time) #resort events by time
            
            # If there are waiting calls, start service
            if len(waiting_queue) > 0:
                arrival = waiting_queue.pop(0) #deletes oldest call from delayed calls
                delayed_intervals.append(time-arrival.time)
                events.append(Event("departure", time + exponential_time(mu))) #we can only generate a new departure when we free space in our channel, this is when a departure happens
            else: # If there are no waiting calls, free a channel
                channels_occupied -= 1
    #For Erlang-B
    blocking_prob = blocked_calls / total_calls
    #For Erlang-C   
    over_Am = 0
    if(queue_length!=0):
        delayed_prob = delayed_calls / total_calls    
        average_delay = sum(delayed_intervals) / total_calls
        for delay in delayed_intervals:
            if(delay<max_delay):
                over_Am +=1
        prob_over_Am =  over_Am / len(delayed_intervals)
        return delayed_prob, average_delay, prob_over_Am
    else:#return blocking probability
        return blocking_prob
    
def plot_results(delayed_intervals, delta, Max, filename=None):
    bins = []
    current_bin = 0

    while current_bin < Max:
        bins.append(current_bin)
        current_bin += delta

    bins.append(Max)  # Ensure the final bin includes values up to Max
    plt.hist(delayed_intervals, bins=bins, edgecolor='black', alpha=0.6, color='g')

    # Plot the exponential distribution
    lambda_ = 1 / (sum(delayed_intervals) / len(delayed_intervals))  # Estimate lambda from the data
    x = np.linspace(0, Max, 1000)
    y = len(delayed_intervals) * lambda_ * np.exp(-lambda_ * x) * delta  # Scale the y-values to match the histogram
    plt.plot(x, y, 'r-', lw=2, label='Exponential Distribution')

    plt.xlabel('Delay Time Intervals')
    plt.ylabel('Number of Calls')
    plt.title('Histogram of Delay Packets')
    plt.legend()
    plt.show()
    
##############################
############ MAIN ############
##############################

lambda_ = 200  # Arrival rate: calls per time unit
mu = 1/0.008   # Service rate: calls handled per time unit
channels = 2 # Number of channels in the system
simulation_calls = 10000
queue_length = 10 #queue length, 0 for Erlang-B, -1 for Erlang-C and any other intenger for the general case
V_min = 1/2 *  1/lambda_ # for ploting the results
Max = 20 * 1/lambda_ # for ploting the results
delayed_intervals = [] #for Erlang-C
data=[]

print("=============================================================")


print("Channels: ", channels, " Queue Length: ", queue_length)

average_delay_prob = []
average_delay = []
average_srv_lvl = []
n=15
sl=20
c=6
with open("simulation_results.csv", "w") as fileopen:
    
    fileopen.write("Lambda, mu, Channel Capacity, Queue Length, Delayed Probability,Average Delay,Service Level,\n")

    # for k in range(1,sl):
    #     for j in range(1,c):
    #         print("Running ", n, " simulations with parameters: \n\tLambda: ", lambda_, "\n\tmu:", mu,"\n\tChannel Capacity: ", j,"\n\tQueue length:" , k)
    #         for i in range(1,n):
    #             data=(simulation( lambda_, mu, j, simulation_calls, k, delayed_intervals))
    #             average_delay_prob.append(data[0])
    #             average_delay.append(data[1])
    #             average_srv_lvl.append(data[2])
            
    #         fileopen.write("{:.2f},{:.2f},{},{},{:.2f},{:.2f},{:.2f}\n".format(lambda_, mu, j, k, sum(average_delay_prob)/(n-1), np.average(average_delay), sum(average_srv_lvl)/(n-1)))
                
    #         average_delay_prob.clear()
    #         average_delay.clear()
    #         average_srv_lvl.clear()
    
    simulation( lambda_, mu, channels, simulation_calls, queue_length, delayed_intervals, max_delay=0.05)
            
if(queue_length==0):
    print("\tBlocking probability: ", data*100, "%")
# else:
#     print("\tProbability that a packet is delayed: {:.2f}%".format(sum(average_delay_prob)/n*100), "+-", np.std(average_delay_prob))
#     print("\tAverage Delay: ", sum(average_delay)/n, "+-", np.std(average_delay))
#     print("\tService Level: {:.2f}%".format(sum(average_srv_lvl)/n *100),"+-", np.std(average_srv_lvl))
    
print("=============================================================")

if(queue_length!=0):
    plot_results(delayed_intervals, V_min, Max)