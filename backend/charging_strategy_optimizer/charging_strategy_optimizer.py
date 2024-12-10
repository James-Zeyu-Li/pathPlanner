# -*- coding: utf-8 -*-

# charging_strategy_optimizer.py

import json
from collections import defaultdict

def load_car(filename, car_type):
    #Loads car parameters from a JSON file

    with open(filename, 'r') as file:
        cars_data = json.load(file)
    
    if car_type not in cars_data:
        raise ValueError(f"Car type '{car_type}' not found in {filename}")
    
    return cars_data[car_type]

def load_path_planner(segment_distances):
    #Loads segment distances and converts them to charging station data for optimization

    charging_stations = []
    for i, segment in enumerate(segment_distances):
        start, end, distance = segment
        charging_stations.append({
            'name': start,
            'distance_to_next': distance
        })
    # Add the final destination without distance
    charging_stations.append({'name': segment_distances[-1][1]})
    return charging_stations

def optimize_charging_strategy(charging_stations, vehicle_params, charging_curve):
    # Initialize SoC levels (0% to 100% in 10% increments)
    soc_levels = [i for i in range(0, 101, 10)]

    # Initialize DP table
    dp_table = initialize_dp_table(len(charging_stations), soc_levels)

    # Set initial state at the starting point
    initial_soc = vehicle_params['current_battery_level']
    dp_table[0][initial_soc] = {'time': 0, 'prev_state': None, 'charge': 0, 'charging_time': 0, 'driving_time': 0}

    # Perform dynamic programming iteration
    dp_table = dynamic_programming_iteration(
        dp_table, charging_stations, vehicle_params, soc_levels, charging_curve
    )

    # Print segment distances for debugging
    print("Segment Distances:")
    for segment in charging_stations[:-1]:
        print(f"From {segment['name']} to next station, Distance: {segment['distance_to_next']} km")

    # Reconstruct the optimal charging strategy
    optimal_strategy, total_time, total_charging_time, total_driving_time = reconstruct_optimal_path(dp_table, charging_stations)

    return optimal_strategy, total_time, total_charging_time, total_driving_time

def initialize_dp_table(num_stations, soc_levels):

    #Initializes the DP table as a list of dictionaries.

    dp_table = []
    for station_index in range(num_stations):
        dp_table.append({})
    return dp_table

def calculate_energy_needed(distance, energy_consumption_rate, battery_capacity):

    #Calculates the energy needed (in SoC percentage) to travel a certain distance.
    energy_needed = (distance / energy_consumption_rate) / battery_capacity * 100  # As a percentage
    # Round to nearest multiple of 10%
    energy_needed = round(energy_needed / 10) * 10
    return energy_needed

def calculate_charging_time(soc_start, soc_end, battery_capacity, charging_curve):
    
    #Calculates the charging time from soc_start to soc_end based on the charging curve.
    
    soc_start = int(round(soc_start / 10) * 10)
    soc_end = int(round(soc_end / 10) * 10)
    charging_time = 0
    for soc in range(soc_start, soc_end, 10):
        power = charging_curve.get(str(soc))
        if power == 0:
            continue  # Cannot charge beyond 100%
        energy_increment = 0.1 * battery_capacity  # 10% of battery capacity
        time_increment = energy_increment / power  # Time = Energy / Power
        charging_time += time_increment
    return charging_time

def dynamic_programming_iteration(dp_table, charging_stations, vehicle_params, soc_levels, charging_curve):
    battery_capacity = vehicle_params['battery_size']
    energy_consumption_rate = vehicle_params['range_per_kw']
    driving_speed = vehicle_params.get('driving_speed', 100)  # Default to 100 km/h

    num_stations = len(charging_stations)

    for i in range(num_stations - 1):
        current_station = charging_stations[i]
        next_station = charging_stations[i + 1]
        distance = current_station['distance_to_next']
        energy_needed = calculate_energy_needed(distance, energy_consumption_rate, battery_capacity)
        travel_time = distance / driving_speed

        updated = False  # Flag to track if any state is updated in this stage

        for soc_current in dp_table[i]:
            cumulative_time = dp_table[i][soc_current]['time']

            # Possible charging decisions (in 10% increments)
            max_charge = 100 - soc_current
            charge_options = [c for c in range(0, int(max_charge) + 1, 10)]  # In 10% increments

            for charge in charge_options:
                soc_charged = soc_current + charge

                # Only try those charging options that can reach the next station
                if soc_charged < energy_needed:
                    continue  

                soc_next = soc_charged - energy_needed
                soc_next = int(round(soc_next / 10) * 10)  # Round to nearest multiple of 10%
                soc_next = max(0, min(100, soc_next))  # Ensure soc_next is within 0% to 100%

                # Calculate charging time
                t_charge = calculate_charging_time(soc_current, soc_charged, battery_capacity, charging_curve)

                # Total time for this path
                total_time = cumulative_time + t_charge + travel_time

                soc_next_int = int(soc_next)
                # Update DP table if this path is better
                if soc_next_int not in dp_table[i + 1] or total_time < dp_table[i + 1][soc_next_int]['time']:
                    dp_table[i + 1][soc_next_int] = {
                        'time': total_time,
                        'prev_state': (i, soc_current),
                        'charge': charge,
                        'charging_time': t_charge,
                        'driving_time': travel_time
                    }
                    updated = True 

        # If no feasible states were found for this stage, force a full charge
        if not updated:
            soc_current = 100  # Assume we start fully charged
            if soc_current >= energy_needed:
                soc_next = soc_current - energy_needed
                travel_time = distance / driving_speed
                total_time = dp_table[i].get(100, {'time': 0})['time'] + travel_time

                dp_table[i + 1][int(soc_next)] = {
                    'time': total_time,
                    'prev_state': (i, soc_current),
                    'charge': 0,  # Assume no extra charging needed as we started fully charged
                    'charging_time': 0,
                    'driving_time': travel_time
                }
                print(f"Warning: No feasible states for stage {i + 1}, forcing full charge at {current_station['name']}.")

    return dp_table


def reconstruct_optimal_path(dp_table, charging_stations):
    final_stage_index = len(charging_stations) - 1
    min_time = float('inf')
    optimal_final_soc = None

    # Find the optimal final SoC
    for soc, data in dp_table[final_stage_index].items():
        if data['time'] < min_time:
            min_time = data['time']
            optimal_final_soc = soc

    if optimal_final_soc is None:
        raise ValueError("No feasible path found to the final stage. Please check the route distances and vehicle parameters.")

    print(f"Optimal final SoC found: {optimal_final_soc} with minimum time: {min_time}")

    # Reconstruct the path
    optimal_strategy = []
    current_stage_index = final_stage_index
    current_soc = optimal_final_soc
    total_charging_time = 0
    total_driving_time = 0

    while current_stage_index > 0:
        state_info = dp_table[current_stage_index].get(current_soc)
        if not state_info:
            raise ValueError(f"Failed to find a feasible state for stage {current_stage_index} with SoC {current_soc}.")

        prev_stage_index, prev_soc = state_info['prev_state']
        charge_amount = state_info['charge']
        charging_time = state_info.get('charging_time', 0)
        driving_time = state_info.get('driving_time', 0)

        # Accumulate the total charging and driving times
        total_charging_time += charging_time
        total_driving_time += driving_time

        # Add to the strategy
        optimal_strategy.insert(0, {
            'station': charging_stations[prev_stage_index]['name'],
            'charge_amount': charge_amount,
            'departure_soc': prev_soc + charge_amount
        })
        current_stage_index = prev_stage_index
        current_soc = prev_soc

    total_time = dp_table[final_stage_index][optimal_final_soc]['time']
    print("Reconstructed optimal path successfully.")
    return optimal_strategy, total_time, total_charging_time, total_driving_time


def traditional_strategy(charging_stations, vehicle_params, charging_curve):
    battery_capacity = vehicle_params['battery_size']
    energy_consumption_rate = vehicle_params['range_per_kw']
    driving_speed = vehicle_params.get('driving_speed', 100)  # Default to 100 km/h
    current_soc = vehicle_params['current_battery_level']
    total_time = 0
    total_charging_time = 0
    total_driving_time = 0
    strategy = []

    for i in range(len(charging_stations) - 1):
        current_station = charging_stations[i]
        distance = current_station['distance_to_next']
        energy_needed = calculate_energy_needed(distance, energy_consumption_rate, battery_capacity)
        travel_time = distance / driving_speed
        total_driving_time += travel_time

        if current_soc < energy_needed:
            # Need to recharge fully
            charge_needed = 100 - current_soc
            charging_time = calculate_charging_time(current_soc, 100, battery_capacity, charging_curve)
            total_time += charging_time
            total_charging_time += charging_time
            strategy.append({
                'station': current_station['name'],
                'charge_amount': int(charge_needed), 
                'departure_soc': int(100) 
            })
            current_soc = 100 


        current_soc -= energy_needed
        total_time += travel_time

    return strategy, total_time, total_charging_time, total_driving_time



def calculate_charging_time_traditional(soc_start, soc_end, battery_capacity, charging_curve):

   # Calculates the charging time for the traditional strategy

    charging_time = 0
    soc_start = int(round(soc_start / 10) * 10)
    soc_end = int(round(soc_end / 10) * 10)

    for soc in range(soc_start, soc_end, 10):
        power = charging_curve.get(str(soc))
        if power == 0:
            continue  
        energy_increment = 0.1 * battery_capacity  # 10% of battery capacity
        time_increment = energy_increment / power  
        charging_time += time_increment
    return charging_time
