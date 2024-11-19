import random
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class Event:
    id: int
    event_type : str #arrival, departure, transition or specific_departure
    goal_system : str #general or area_specific
    time : float #time in which the event occurs or the duration of the call

class Calls:
    def exponential_time(const):
        return -math.log(1.0 - random.random()) / const
    
    
    def generate_arrival(id,time, lambda_): #Generate an arrival event
        call_type = random.choices(['general', 'area_specific'], weights=[0.3, 0.7])[0] #Choose the call type, with 30% being general and 70% being area specific

        return Event(id,"arrival", call_type, time+Calls.exponential_time(lambda_))
    
    def generate_departure(id,time, goal_system, event_type="normal", ): #Generate a departure event
        if goal_system == "general": #If the call is general, generate a general purpose call duration
            return Event(id,"departure", "general", time+Calls.calculate_general_purpose())
        elif (goal_system == "area_specific" and event_type=="normal"): #If the call is area specific, generate an area specific call duration
            return Event(id,"departure", "area_specific", time +Calls.calculate_area_specific_gaussian_call())
        elif (goal_system == "area_specific" and event_type=="transition"): #If the call is area specific, generate an area specific call duration
            return Event(id,"transition", "area_specific", time+Calls.calculate_area_specific_call())
        

    
    def calculate_general_purpose():
        min_duration = 1
        avg_exponential_time = 1/2  #for 30% of the calls
        
        additional_duration = Calls.exponential_time(avg_exponential_time)

        while(additional_duration > 4): # Repeat if total duration is greater than 5
            additional_duration = Calls.exponential_time(avg_exponential_time)

        total_duration = min_duration + additional_duration
        
        return total_duration*60 # Ensure the duration is within the min and max values

    def calculate_area_specific_gaussian_call():
        avg_duration = 60
        std_dev = 20
        
        # Generate a duration following the Gaussian distribution
        duration = random.gauss(avg_duration, std_dev)
        
        while(duration > 120 or duration < 30): # Ensure the duration is within the min and max values
            duration = random.gauss(avg_duration, std_dev)

        return duration

    def calculate_area_specific_call():
        avg_duration = 1/150 #2.5 min
        min_duration = 60

        duration = min_duration + Calls.exponential_time(avg_duration)

        return duration


class Plot:
    def plot_results(arrival_times, delta, Max, Title, xlabel):
        bins = []
        current_bin = 0

        while current_bin < Max:
            bins.append(current_bin)
            current_bin += delta

        bins.append(Max)  # Ensure the final bin includes values up to Max
        plt.hist(arrival_times, bins=bins, edgecolor='black', alpha=0.6, color='g')

        # Plot the gaussian distribution distribution
        # mu = np.mean(arrival_times)
        # sigma = np.std(arrival_times)
        # x = np.linspace(min(arrival_times), max(arrival_times), 100)
        # y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        # plt.plot(x, y * len(arrival_times) * delta, color='r', label='Gaussian Distribution')

        plt.xlabel(xlabel)
        plt.ylabel('Number of Calls')
        plt.title(Title)
        plt.legend()
        plt.show()
        
    
            