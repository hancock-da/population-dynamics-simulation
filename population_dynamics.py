""" 
Program to simulate population dynamics of breeding rabbits and predator foxes in a closed system.
    1. If a fox (red dot) comes into contact with a rabbit (blue dot) it will eat it.
    2. Rabbits can breed when they come into contact 
    3. Rabbits have a population carrying capacity (max) of 50 individuals. Any more will die.
    4. This program has multiple options:
        a) If you just want to watch a single simulation of foxes eating rabbits choose 'y' for the first input.
        b) If you want to test the half life of rabbits in simulations with evolutionary strategies at different run speeds, 
        choose 'n' for the first input and 'speed' for the second input
        c) If you want to test the success of rabbits vs foxes (can rabbits persist in the system) over 100 simulations,
        choose 'n' for the first input and 'success' for the second input
"""
import math
import matplotlib.pyplot as plt
import random
import numpy as np

# lists you want to be accessible from all parts of your code are:
global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, start_rabbits, rabbits_count, positions_foxes_x, positions_foxes_y, fox_speed, foxes_angles, timestep, time, rabbits_per_timestep, frac_living_rabbits, avg_half_life
#-------------------
def predator_prey():
#-------------------

    # retrieve the 'shared' lists defined above
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, start_rabbits, rabbits_count, positions_foxes_x, positions_foxes_y, number_foxes, fox_speed, foxes_angles, timestep, time, rabbits_per_timestep, frac_living_rabbits, sim

    # "y" for animation, "n" if not
    sim = sim

    timestep = 0
    # define the starting position of rabbits (x-position and y-position at t=0)
    positions_rabbits_x = []  
    positions_rabbits_y = []
    start_rabbits = 25

    positions_foxes_x = [70, 80]
    positions_foxes_y = [70, 80]
    # In case we want to randomly assign a number of foxes with starting positions
    number_foxes = 2 

    # For each rabbit, give a random starting location in a (20,30) (x,y) grid
    for rabbit in range(0,start_rabbits):
        x = random.uniform(20,30)
        y = random.uniform(20,30)
        positions_rabbits_x.append(x)
        positions_rabbits_y.append(y)

    # Define a random angle for each rabbit to move
    rabbits_angles = []
    for rabbit in range(start_rabbits):
        angle = 2 * math.pi * random.random()
        rabbits_angles.append(angle)
    
    # Define intial angles for each fox to move in
    foxes_angles = []
    fox_count = len(positions_foxes_x)
    for fox in range(fox_count):
        angle = 2*math.pi*random.random()
        foxes_angles.append(angle)

    # Empty list to record the number of rabbits at each timestep for plotting
    rabbits_per_timestep = []

    # Empty list to store the fraction of rabbits remaining at each timestep for plotting
    frac_living_rabbits = []

    # Empty list for plotting time
    time = []

    # take steps in time
    for i_time in range(1000):
        timestep += 1
    
        # move the foxes
        move_foxes()

        # move the rabbits
        move_rabbits()   

        # foxes eat rabbits that get too close
        dinnertime()

        # Keep track of number and fraction of rabbits and timesteps for plotting
        tracker()

        # After 200 timesteps, rabbits that are close together reproduce
        if timestep >= 200:
            reproducing_rabbits()
            overpopulation()

        if sim == "y":
            # plot the position of the rabbits
            draw_forest()
        else:
            continue

    return rabbits_per_timestep

#---------------------------
def move_foxes():
#---------------------------
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, rabbits_count, positions_foxes_x, positions_foxes_y, fox_speed, foxes_angles, timestep

    fox_speed = 2

    # Move foxes according to speed and angle
    fox_count = len(positions_foxes_x)
    for fox in range(fox_count):
        angle = foxes_angles[fox]
        velocity_x = fox_speed*math.cos(angle)
        velocity_y = fox_speed*math.sin(angle)
        positions_foxes_x[fox] = positions_foxes_x[fox] + velocity_x
        positions_foxes_y[fox] = positions_foxes_y[fox] + velocity_y

        # Stop foxes moving past the edges of the forest by reverting direction
        if positions_foxes_x[fox] < 0 or positions_foxes_x[fox] > 100 or positions_foxes_y[fox] < 0 or positions_foxes_y[fox] > 100:
            new_angle = angle + math.pi
            foxes_angles[fox] = new_angle
            new_velocity_x = fox_speed*math.cos(new_angle)
            new_velocity_y = fox_speed*math.sin(new_angle)
            positions_foxes_x[fox] = positions_foxes_x[fox] - velocity_x + new_velocity_x
            positions_foxes_y[fox] = positions_foxes_y[fox] - velocity_y + new_velocity_y

        # Each run, generate new random direction from normal distribution around original angle
        # Width of normal distribution (0.2) determines how easy it is for fox to move away from original direction
        angle_new = np.random.normal(foxes_angles[fox], 0.2)
        foxes_angles[fox] = angle_new
        

#---------------------------
def move_rabbits():
#---------------------------

    # retrieve the 'shared' lists defined above
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, rabbits_count, positions_foxes_x, positions_foxes_y, fox_speed, foxes_angles, timestep
    
    if strategy == "s":
        rabbit_speed = 1

    # move the rabbits in a random direction
    rabbits_count = len(positions_rabbits_x)   
    for rabbit in range(rabbits_count):

        # Each run, give a 1/20 chance for the rabbit to stop and change angle
        freeze_prob = random.uniform(0,1)
        if freeze_prob < 0.05:
            rabbits_angles[rabbit] = 2*math.pi*random.random()
            continue
        
        angle = rabbits_angles[rabbit]
        
        velocity_x = rabbit_speed*math.cos(angle)
        velocity_y = rabbit_speed*math.sin(angle)
        
        # Move the rabbit in x and y by speed*direction
        positions_rabbits_x[rabbit] = positions_rabbits_x[rabbit] + velocity_x
        positions_rabbits_y[rabbit] = positions_rabbits_y[rabbit] + velocity_y
        
        # Stop rabbits moving past the edges of the forest by reverting direction
        if positions_rabbits_x[rabbit] < 0 or positions_rabbits_x[rabbit] > 100 or positions_rabbits_y[rabbit] < 0 or positions_rabbits_y[rabbit] > 100:
            new_angle = angle + math.pi
            rabbits_angles[rabbit] = new_angle
            new_velocity_x = rabbit_speed*math.cos(new_angle)
            new_velocity_y = rabbit_speed*math.sin(new_angle)
            positions_rabbits_x[rabbit] = positions_rabbits_x[rabbit] - velocity_x + new_velocity_x
            positions_rabbits_y[rabbit] = positions_rabbits_y[rabbit] - velocity_y + new_velocity_y

#--------------------------
def dinnertime():
#--------------------------
    
    # retrieve shared defined lists
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, rabbits_count, positions_foxes_x, positions_foxes_y, fox_speed, foxes_angles, timestep

    fox_count = len(positions_foxes_x)

    for rabbit in range(rabbits_count-1,-1,-1):
        count = 0
        for fox in range(fox_count):
            if count == 0:
                dist = math.sqrt((positions_rabbits_x[rabbit] - positions_foxes_x[fox])**2 + (positions_rabbits_y[rabbit] - positions_foxes_y[fox])**2)
                if dist <= 5:
                    del positions_rabbits_x[rabbit], positions_rabbits_y[rabbit], rabbits_angles[rabbit]
                    count += 1

#--------------------------
def tracker():
#--------------------------
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, start_rabbits, rabbits_count, positions_foxes_x, positions_foxes_y, fox_speed, foxes_angles, timestep, time, rabbits_per_timestep, frac_living_rabbits, rabbits_remaining

    # Calculate the number of rabbits remaining per timestep
    rabbits_remaining = len(positions_rabbits_x)
    # Append the number of rabbits at each second to a list
    rabbits_per_timestep.append(rabbits_remaining)

    # Calculate the fraction of rabbits remaining per timestep
    fraction_rabbits = rabbits_remaining/start_rabbits*100
    # Append the fraction of rabbits remaining to a list
    frac_living_rabbits.append(fraction_rabbits)

    # Append the current timestep the time list
    time.append(timestep)

#--------------------------
def reproducing_rabbits():
#--------------------------
    global positions_rabbits_x, positions_rabbits_y, rabbits_angles, rabbits_remaining

    # Create a counter to prevent rabbits reproducing too many times per meeting
    count = 0

    # For each rabbit, check distance to each other rabbit. If distance is <1m, produce 4 new rabbits in random positions
    for rabbit1 in range(rabbits_remaining-1):
        for rabbit2 in range(rabbits_remaining-1):
            if rabbit1 == rabbit2:
                pass
            elif count == 0:    
                dist = math.sqrt((positions_rabbits_x[rabbit2] - positions_rabbits_x[rabbit1])**2 + (positions_rabbits_y[rabbit2] - positions_rabbits_y[rabbit1])**2)
                if dist <= 1:
                    for nest in range(4):
                        positions_rabbits_x.append(random.randrange(0,100,1))
                        positions_rabbits_y.append(random.randrange(0,100,1))
                        rabbits_angles.append(2*math.pi*random.random())
                        count += 1


#--------------------------
def overpopulation():
#--------------------------
     
    global positions_rabbits_x, positions_rabbits_y, rabbits_angles, rabbits_count

    list_length = len(positions_rabbits_x)
    if list_length > 50:
        del positions_rabbits_x[50:], positions_rabbits_y[50:], rabbits_angles[50:]


#--------------------------
def draw_forest():
#--------------------------

    # retrieve the 'shared' lists defined above
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, rabbits_count, positions_foxes_x, positions_foxes_y, fox_speed, foxes_angles, timestep

    # define the axes of the forest
    plt.axis([0, 100, 0, 100])

    # draw the rabbits (blue dot)
    plt.plot(positions_rabbits_x, positions_rabbits_y, 'o', color = 'blue', markersize = 6)

    # draw the foxes (red dot)
    plt.plot(positions_foxes_x, positions_foxes_y, 'o', color = 'red', markersize = 10)

    plt.text(10,10, "seconds: %.0f" % timestep)
    
    # update the frames (for a simple animation)
    plt.draw()        
    plt.pause(0.001)
    # plt.show()
    plt.clf()

#--------------------------
def success_chance_rabbits():
#--------------------------

    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, start_rabbits, rabbits_count, positions_foxes_x, positions_foxes_y, number_foxes, fox_speed, foxes_angles, timestep, time, rabbits_per_timestep, frac_living_rabbits, number_runs, avg_half_life, strategy
    
    # Set the number of times the simulation is run
    number_runs = number_runs
    
    # Create an empty list to store the winner of each simulation
    winner_per_run = []
    
    # For n runs, find the timestep at which half of the rabbits have been eaten.
    for run in range(number_runs):
        rabbits_per_timestep = predator_prey() 
    
        # If a single speed strategy is tested, print every 25 runs to show progress.
        if number_runs >= 100:
            if run % 25 == 0:
                print("Simulation number:",run)

        if rabbits_per_timestep[-1] >= 45:
            winner = "Rabbits"
        elif rabbits_per_timestep[-1] <= 5:
            winner = "Foxes"
        else:
            winner = "Tie"

        # If the number of runs is 1, plot the results of the simulation including the half life.
        if number_runs == 1:
            print("The number of rabbits after t =", max(time), "steps was", rabbits_per_timestep[-1])
            print("This means that the", winner, "have won.")
            
            redbox = dict(boxstyle='square', facecolor='red', alpha=0.5)

            plt.plot(time, rabbits_per_timestep, 'b-')
            plt.axhline(y=start_rabbits, color = 'r', linestyle = '--')
            plt.ylim(0, 60)
            plt.xlim(0, max(time))
            plt.text(450, start_rabbits+2, "Number of rabbits over time")
            plt.text(450, start_rabbits-3, "Forest(100), N_rabbits=" + str(start_rabbits) + ", N_foxes=" + str(number_foxes))
            plt.text(450, 12, winner + " win", fontsize = 15, bbox = redbox)
            plt.xlabel("Time (seconds)")
            plt.ylabel("Number of living rabbits")
            plt.show()
        
        if number_runs > 1:
            winner_per_run.append(winner)
    
    success_chance = winner_per_run.count("Rabbits") / len(winner_per_run) * 100

    print("A simulated world with: N_rabbits = ", start_rabbits, "(speed=",rabbit_speed,"m/s)", "N_fox = ",number_foxes, "(speed=", fox_speed, "m/s)", "N_simulations = ", number_runs)
    print("In", success_chance, "percent of the cases the rabbits win")


    return


#--------------------------
def average_half_life():
#--------------------------
    global positions_rabbits_x, positions_rabbits_y, rabbit_speed, rabbits_angles, start_rabbits, rabbits_count, positions_foxes_x, positions_foxes_y, number_foxes, fox_speed, foxes_angles, timestep, time, rabbits_per_timestep, frac_living_rabbits, number_runs, avg_half_life, strategy

    half_life = 0
    number_runs = number_runs
    half_life_per_run = []
    
    # For n runs, find the timestep at which half of the rabbits have been eaten.
    for run in range(number_runs):
        rabbits_per_timestep = predator_prey()

        # Calculate half the number of initial rabbits.
        half_rabbits = round(start_rabbits/2)
        # Set a stop variable to stop once half life has been evaluated for the first time this run.
        half_life_stop = 0
        
        # Find which timestep the number of rabbits reaches half the starting number
        for i,rabbit in enumerate(rabbits_per_timestep):
            if half_life_stop == 0:
                if rabbit == half_rabbits:
                    half_life = i
                    half_life_stop +=1
        
        half_life_per_run.append(half_life)

        # If a single speed strategy is tested, print every 25 runs to show progress.
        if strategy == "s" and number_runs >= 100:
            if run % 25 == 0:
                print("Simulation number:",run)
    
    # Calculate the average half life over all runs.
    avg_half_life = sum(half_life_per_run)/len(half_life_per_run)
    
    # If a single speed strategy is tested, print the average half life
    if strategy == "s":
        print("A simulated world with: N_rabbits =",start_rabbits,"N_fox =",number_foxes,"N_simulations =",number_runs)
        if half_life == 0:
            print("Rabbit population not halved. Increase number of time steps.")
        else:
            print("Average half-life of rabbits =",avg_half_life,"seconds")

        # If the number of runs is 1, plot the results of the simulation including the half life.
        if number_runs == 1:
            if half_life != 0:
                print("After", half_life, "seconds, more than half the rabbits have been eaten")

            plt.plot(time, frac_living_rabbits, 'b-')
            plt.plot(half_life, 50, 'ro')
            plt.ylim(0,max(frac_living_rabbits)+10)
            plt.xlim(0, max(time))
            if half_life != 0:
                plt.annotate("T (half) = %.0f" % half_life, (half_life+10, 55))
            plt.text(150, 95, "Fraction of living rabbits over time")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Fraction living rabbits")
            plt.show()
        
    return avg_half_life

#--------------------------
def speed_strategies():
#--------------------------
    global rabbit_speed, strategy_speeds, start_rabbits, number_foxes, number_runs, avg_half_life, strategy

    # Change strategy to "m" for multiple or "s" for single
    strategy = strategy
     # A list of different speeds to test
    strategy_speeds = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 5.0]
    # An empty list to store the average half life per speed strategy
    strategy_avg_half_life = []

    
    # If strategy = s, run average half life with rabbit speed 1 (default).
    # Otherwise, for each speed in the list of strategies, run average half life and append to list.
    for speed in range(0,len(strategy_speeds)):
        if strategy == "s":
            rabbit_speed = 1
            average_half_life()
            break
        else:
            rabbit_speed = strategy_speeds[speed]
            strategy_avg_half_life.append(average_half_life())
            print("Rabbit speed = ",rabbit_speed,"m/s -> Average half-life of rabbits =",avg_half_life)
    
    return strategy_avg_half_life


#====================
#== Main program ==
#====================
watch = input("Would you like to simply watch a single simulation of population dynamics? please type y or n ")
if watch == 'y':
    sim = 'y'
    strategy = 's'
    number_runs = 1
    average_half_life()
if watch == 'n':
    sos = input("Would you like to test rabbit (speed) strategies over 20 simulations per strategy or test rabbit success (persistence) rates over 100 simulations? Type speed or success: ")
    sim = 'n'
    if sos == 'speed':
        strategy = 'm'
        number_runs = 20
        speed_strategies()
    elif sos == 'success':
        number_runs = 100
        strategy = 's'
        success_chance_rabbits()
    else:
        input("please type 'speed' or 'success' ")
