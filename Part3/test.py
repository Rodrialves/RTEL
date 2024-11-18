import random
import math
import matplotlib.pyplot as plt
import numpy as np
import funtions as f

queue_size = 5 #value for testing
lambda_ = 80/3600 #FIX (Its in calls/hour)
# general resource = 1 , area specific resource = 1, queue = 5 
current_time = 0
active_calls = 0  # Number of currently active calls
total_calls = 0  # Total number of call attempts
dropped_calls = 0  # Track dropped calls
gp_queue = []  # List of active call events in general purpose (start, end times, and call type)
gp_operators = 1
area_specific_operators = 5
operator = 0
gp_active_calls = 0
# To track data for plotting
time_data = []  # Track current time
active_calls_data = []  # Number of active calls over time
accepted_calls = 0  # Calls that were accepted and not dropped

# Separate queue for area-specific calls
area_specific_queue = []
area_specific_active_calls = 0

# Generate initial call arrival time
call_time = f.exponential_time(lambda_)
next_call_arrival = call_time

while total_calls < 1000:  # Example total calls target
    if next_call_arrival <= current_time:
        total_calls += 1
        call_type = random.choices(['general', 'area_specific'], weights=[0.3, 0.7])[0]
        if call_type == 'general':
            call_duration = f.calculate_general_purpose()
        else:
            call_duration = f.calculate_area_specificgp_call()
        
        if active_calls < queue_size and gp_active_calls < gp_operators:
            call_end_time = current_time + call_duration
            gp_queue.append((call_end_time, call_type, 1)) #1 indicates its an atual active call with an operator answering
            active_calls += 1
            accepted_calls += 1
            gp_active_calls +=1
        elif active_calls < queue_size and gp_active_calls >= gp_operators:
            call_end_time = current_time + call_duration
            gp_queue.append((call_end_time, call_type, 0))
            active_calls += 1
            accepted_calls += 1
        else:
            dropped_calls += 1
        
        call_time = f.exponential_time(lambda_)
        next_call_arrival = next_call_arrival + call_time
    else:
        if gp_queue:
            gp_queue.sort()
            next_call_end_time, call_type, operator = gp_queue.pop(0)
            current_time = next_call_end_time
            active_calls -= 1
            if operator == 1 and call_type == 'area_specific':
                if area_specific_active_calls < area_specific_operators:
                    #no queue for area specific calls
                    area_specific_duration = f.calculate_area_specific_call()
                    area_specific_end_time = current_time + area_specific_duration
                    area_specific_queue.append(area_specific_end_time)
                    area_specific_active_calls += 1
                else :
                    gp_queue.append((current_time, 'area_specific',1))
                    active_calls += 1
                    current_time = next_call_arrival
            elif operator == 0:
                gp_queue.append((current_time,call_type,0))
                active_calls += 1
                current_time = next_call_arrival
        else:
            current_time = next_call_arrival

    time_data.append(current_time)
    active_calls_data.append(active_calls)

    # Process area-specific queue
    if area_specific_queue:
        area_specific_queue.sort()
        next_area_specific_end_time = area_specific_queue[0]
        if next_area_specific_end_time <= current_time:
            area_specific_queue.pop(0)
            area_specific_active_calls -= 1

blocking_probability = dropped_calls / total_calls if total_calls > 0 else 0
print(f"Blocking Probability: {blocking_probability:.2f}")
print(area_specific_active_calls)