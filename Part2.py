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

def simulation(lamba_, mu, channels, simulation_calls, queue_length, max_delay=0.5):
    # Initialize the simulation
    time = 0
    events = []
    
    channels_occupied = 0
    blocked_calls = 0
    
    waiting_queue = []
    delayed_calls = 0
    delayed_intervals = []
    
    total_calls = 0

    print("Run simulation with parameters: \n\tLambda: ", lamba_, "\n\tmu:", mu,"\n\tChannel Capacity: ", channels,"\n\tQueue length:" , queue_length)

    # Generate first call
    events.append(Event("arrival", exponential_time(lamba_)))
    total_calls += 1

    # Start simulation
    while total_calls < simulation_calls:
        # Get the next event
        events.sort(key=lambda events: events.time) #sort events by time
        event = events.pop(0)
        time = event.time
                
        # Process the event
        if event.event_type == "arrival":
            # Generate next arrival event
            events.append(Event("arrival", time + exponential_time(lamba_)))
            total_calls += 1

            # If there are free channels, start service
            if channels_occupied < channels:
                channels_occupied += 1
                events.append(Event("departure", time + exponential_time(mu)))
            # Otherwise, increment blocking calls
            elif((queue_length > 0 and len(waiting_queue) < queue_length) or queue_length==-1):
                waiting_queue.append(event)
                delayed_calls += 1
            else: 
                blocked_calls += 1
                
        elif event.event_type == "departure":
            
            events.sort(key=lambda events: events.time) #resort events by time
            
            if(channels_occupied>0):
                channels_occupied -=1
            # If there are waiting calls, start service
            if len(waiting_queue) > 0:
                arrival = waiting_queue.pop(0) #deletes oldest call from delayed calls
                delayed_intervals.append(time-arrival.time)
                channels_occupied +=1
                events.append(Event("departure", time + exponential_time(mu))) #we can only generate a new departure when we free space in our channel, this is when a departure happens
    
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
    else:
        return blocking_prob
    
##############################
############ MAIN ############
##############################

lamba_ = 200  # Arrival rate: calls per time unit
mu = 1/0.008   # Service rate: calls handled per time unit
channels = 2 # Number of channels in the system
simulation_calls = 10000
queue_length = -1 #queue length, 0 for Erlang-B, -1 for Erlang-C and any other intenger for the general case

print("=============================================================")

data = simulation( lamba_, mu, channels, simulation_calls, queue_length)

print("Resulsts:")
if(queue_length==0):
    print("\tBlocking probability: ", data*100, "%")
else:
    print("\tProbability that a packet is delayed: {:.2f}%".format(data[0]*100))
    print("\tAverage Delay: ", data[1])
    print("\tService Level: {:.2f}%".format(data[2]*100))
    
print("=============================================================")