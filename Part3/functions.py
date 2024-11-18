import random
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class Event:
    event_type : str #arrival, departure, transition or specific_departure
    goal_system : str #general or area_specific
    time : float #time in which the event occurs or the duration of the call

class Calls:
    def exponential_time(const):
        return -math.log(1.0 - random.random()) / const
    
    
    def generate_arrival(time, lambda_): #Generate an arrival event
        call_type = random.choices(['general', 'area_specific'], weights=[0.3, 0.7])[0] #Choose the call type, with 30% being general and 70% being area specific

        return Event("arrival", call_type, time+Calls.exponential_time(lambda_))
    
    def generate_departure(time, goal_system, event_type="normal", ): #Generate a departure event
        if goal_system == "general": #If the call is general, generate a general purpose call duration
            return Event("departure", "general", time+Calls.calculate_general_purpose())
        elif (goal_system == "area_specific" and event_type=="normal"): #If the call is area specific, generate an area specific call duration
            return Event("departure", "area_specific", time +Calls.calculate_area_specific_gaussian_call())
        elif (goal_system == "area_specific" and event_type=="transition"): #If the call is area specific, generate an area specific call duration
            return Event("transition", "area_specific", time+Calls.calculate_area_specific_call())
        

    
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
            