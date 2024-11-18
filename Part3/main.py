# For reference every variable with a "g" is for the general purpose operators 
# and every variable with an "s" is for the area specific operators

import random
from functions import Calls as f, Plot as p


#DEBUG = True #Set to TRUE to print debug information
DEBUG = False #Set to FALSE to not print debug information

PLOT = False #Set to TRUE to plot the results
##############################
######### Simulation #########
##############################

    

def simulation(lambda_=80/3600, Ng=10, Ns=5, Nq=5, sim_calls=13440):
    print("Simulation started with the following parameters:", "\n", "Arrival rate: {:.2f}".format(lambda_), "\n", 
          "Number of general purpose operators: {:.0f}".format(Ng), "\n", "Number of area specific operators: {:.0f}".format(Ns), "\n", 
          "Queue size: {:.0f}".format(Nq), "\n", "Number of calls to simulate: {:.0f}".format(sim_calls))
    
    # Initialize variables of the simulation
    time = 0 #Current time
    total_calls = 0 #Total number of calls
    total_g_calls = 0 #Total number of general purpose calls
    total_s_calls = 0 #Total number of area specific calls
    delayed_g_calls = 0 #Number of delayed general purpose calls
    delayed_s_calls = 0 #Number of delayed area specific calls
    blocked_calls = 0 #Number of blocked calls
    channels_g_occupied = 0 #Number of genral channels occupied
    channels_s_occupied = 0 #Number of area specific channels occupied
    events = [] #List to store the events
    waiting_g_queue = [] #List to store the general waiting queue
    waiting_s_queue = [] #List to store the area specific waiting queue
    waiting_g_intervals = [] #List to store the waiting intervals of the general system
    waiting_s_intervals = [] #List to store the waiting intervals of between the general system arrival and the answer by the area specific system 
    
    # Generate first call
    events.append(f.generate_arrival(time, lambda_))
    total_calls += 1
    
    while total_calls < sim_calls:
        if DEBUG:
            print("=====================================================================")
        #Get the next event in the list
        events.sort(key=lambda events: events.time) #sort events by time
        event = events.pop(0)
        time = event.time
        
        if event.goal_system == "general":
            total_g_calls += 1
        elif event.goal_system == "area_specific":
            total_s_calls += 1
            
        #Process the event
        if event.event_type == "arrival":
            if DEBUG:
                print("Call arrived at time {:.2f}".format(time), "and the expected waiting time is", "TEST", "\nThe goal system of this call is", event.goal_system)
            #Generate next arrival event
            events.append(f.generate_arrival(time, lambda_))
            total_calls += 1
            
            #If there are free general purpose operators, start service
            if channels_g_occupied < Ng:
                channels_g_occupied += 1
                if event.goal_system == "area_specific":
                    events.append(f.generate_departure(time, event.goal_system))
                    duration = events[-1].time - time
                    waiting_s_intervals.append(duration)
                else:
                    events.append(f.generate_departure(time, event.goal_system))
            elif len(waiting_g_queue) < Nq: #If the queue is not full, add the call to the queue
                waiting_g_queue.append(event)
                delayed_g_calls += 1
            else: #If the queue is full, increment the number of blocked calls
                blocked_calls += 1
                
        elif event.event_type == "departure":
            if DEBUG:
                if event.goal_system == "general":
                    print("Call departed from the general system at time {:.2f}".format(time))
                elif event.goal_system == "area_specific":
                    print("Call routed to the area specific system at time {:.2f}".format(time))
            
            if len(waiting_g_queue) > 0: #If there are waiting calls, start service
                arrival = waiting_g_queue.pop(0) # serves the oldest call in the queue
                waiting_g_intervals.append(time-arrival.time)
                
                if(arrival.goal_system == "area_specific"): #If the call is area specific, store the delay interval
                    waiting_s_intervals.append(time-arrival.time)
                    
                events.append(f.generate_departure(time, arrival.goal_system))
            else: #If there are no waiting calls, free one channel
                channels_g_occupied -= 1
                
            if event.goal_system == "area_specific":
                if channels_s_occupied < Ns: #If there are free area specific operators, start service
                    channels_s_occupied += 1
                    events.append(f.generate_departure(time, "area_specific","transition"))
                else: #Add the call to the queue, given that the channels are occupied
                    waiting_s_queue.append(event)
                    delayed_s_calls += 1
        elif event.event_type == "transition":
            if DEBUG:
                print("Call departed from the area specific system at time {:.2f}".format(time))
            if len(waiting_s_queue) > 0: #If there are waiting calls, start service
                arrival = waiting_s_queue.pop(0)
                waiting_s_intervals.append(time-arrival.time)
                events.append(f.generate_departure(time, "area_specific","transition"))
            else: #If there are no waiting calls, free one channel
                channels_s_occupied -= 1
                    
     #specificatin parameters
    p_delayed_g_calls = delayed_g_calls/total_calls*100
    p_blocked_g_calls = blocked_calls/total_calls*100
    aver_g_time = sum(waiting_g_intervals)/len(waiting_g_intervals)
    aver_g_2_s = blocked_calls/total_calls*100
    
    print("=====================================================================",
          "\nSimulation ended with the following results:", "\n", "Total Number of calls.", total_calls,
            "\n Number of blocked calls: {:.0f};".format(blocked_calls), "Probability of blocking: {:.2f} %.".format(p_blocked_g_calls), 
            "\n Number of delayed general purpose calls: {:.0f};".format(delayed_g_calls), "Probability of delay: {:.2f} %.".format(p_delayed_g_calls),
            "\n Number of delayed area specific calls: {:.0f}.".format(delayed_s_calls),
            "\n Average waiting time of general purpose calls: {:.2f} seconds.".format(aver_g_time),
            "\n Average time between arrival to General Purpose system and being answered by Area Specific system: {:.2f} seconds.".format(aver_g_2_s)) 
    
    if PLOT:
        p.plot_results(waiting_g_intervals, 10, max(waiting_g_intervals), "General Purpose System Waiting Times", "Time (s)")
   
    
    
##############################
############ Main ############
##############################

lambda_ = 80/3600 #FIX (Its in calls/hour); Arrival rate: calls per time unit
Ng = 1 #Number of general purpose operators
Ns = 1 #Number of area specific operators
Nq = 5 #Queue size
sim_calls = lambda_*3600*24*7 #Number of calls to simulate, equivalent to 1 week

#Check which values comply with specifications

simulation(lambda_, Ng, Ns, Nq, sim_calls)




