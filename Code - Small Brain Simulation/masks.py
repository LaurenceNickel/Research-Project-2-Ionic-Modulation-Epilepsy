import numpy as np
from brian2 import *

def create_spherical_mask(topology, mask_settings):
    
    x, y, z = topology
    coord_of_stimulus, radius_of_stimulus = mask_settings
    
    stimulus_mask = np.zeros(len(x))

    for neuron_id in range(len(x)):

        distance_xyz = np.sqrt((x[neuron_id] - coord_of_stimulus[0])**2 + ((y[neuron_id] - coord_of_stimulus[1])**2) + ((z[neuron_id] - coord_of_stimulus[2])**2))
        stimulus_mask[neuron_id] = (distance_xyz <= radius_of_stimulus)

    return stimulus_mask

# Cylindrical Mask

# def create_treatment_mask (topology, treatment_settings):
    
#     x, y, z = topology
#     coord_of_electrode, radius_of_electrode, height_of_electrode = treatment_settings
    
#     treatment_mask = zeros(len(x))

#     for neuron_id in range(len(x)):

#         distance_xy = np.sqrt((x[neuron_id] - coord_of_electrode[0])**2 + ((y[neuron_i'd] - coord_of_electrode[1])**2))

#         treatment_mask[neuron_id] = (z[neuron_id] >= coord_of_electrode[2] - height_of_electrode) and (z[neuron_id] <= coord_of_electrode[2] + height_of_electrode) and (distance_xy <= radius_of_electrode)

#     return treatment_mask



# Electrode Mask Position Calculation
# Still very messy need to clean

def calculate_max_distance (first_mask_coord, box_bounds, dim):
    box_bounds_lower, box_bounds_upper = box_bounds
    
    distances_to_lower_bound_x = first_mask_coord[dim] - box_bounds_lower[dim]
    distances_to_upper_bound_x = box_bounds_upper[dim] - first_mask_coord[dim]

    if distances_to_lower_bound_x > distances_to_upper_bound_x:
        max_distance_dir = -distances_to_lower_bound_x
    else:
        max_distance_dir = distances_to_upper_bound_x
    return max_distance_dir

def get_coord_of_electrode(first_mask_coord, box_bounds, distance_between, mask_radius):
    
    if mask_radius*2 > box_bounds[0] or mask_radius*2 > box_bounds[1] or mask_radius*2 > box_bounds[2]:
        raise ValueError('Diameter provided is larger than box size')
        
    box_bounds_lower = np.array([mask_radius]*3)
    box_bounds_upper = np.array(box_bounds) - mask_radius
    box_bounds = [box_bounds_lower, box_bounds_upper]
    
    feasability_check = [lowerb <= c+distance_between <= upperb for lowerb, upperb, c in zip(box_bounds_lower, box_bounds_upper, first_mask_coord)]
    if not all(feasability_check):
        raise ValueError('No feasable solution. The second sphere cannot be fit in the region with the provided distance away from the first mask. Please check the radii and distances of both masks.')
         
    max_distance_x = calculate_max_distance (first_mask_coord, box_bounds, 0)
    max_distance_y = calculate_max_distance (first_mask_coord, box_bounds, 1)
    max_distance_z = calculate_max_distance (first_mask_coord, box_bounds, 2)

    max_vector = np.array([max_distance_x, max_distance_y, max_distance_z])
    max_distance = np.sqrt(np.sum(max_vector ** 2))
    
    print('Radius of electrode:', mask_radius)
    print('Max distance possible between masks:', max_distance)
    print('Distance selected:', distance_between)
    print()

    if distance_between > max_distance:
        raise ValueError('Distance selected is greater than allowed')
    
    direction_vector = max_vector / np.linalg.norm(max_vector)
    
    second_coord = first_mask_coord + direction_vector * distance_between
    
    return second_coord

def populate_electrode_positions (variables):

    coords_of_electrode = []

    for i in range(len(variables['duration'])):
        bounds = variables['bounds'][i]
        print()
        coord = get_coord_of_electrode(variables["coord_of_stimulus"][i], bounds, variables["distance_between_masks"][i], variables["radius_of_electrode"][i])
        coords_of_electrode.append(coord.tolist())
    
    return coords_of_electrode

copy_times = 5
ms = 1000

variables = {

    # Defining the simulation settings.
    "run_id": ['Results 1', 'Results 2', 'Results 3', 'Results 4', 'Results 5'],
    "duration": [4000 * ms] * copy_times,
    "bounds": [[600, 600, 600]] * copy_times,

    # Defining the network settings.
    "N": [[13500, 3375]] * copy_times,  # [N_exc, N_inh]

    # Defining the potassium equilibrium potential for both the excitatory and inhibitory neurons.
    # - Healthy mode: Eke_baseline = -90mV
    # - Epileptic mode: Eke_baseline = -84mV
    "Eke_baseline": [-84 * mV] * copy_times,
    "Eki_baseline": [-90 * mV] * copy_times,

    # Defining the noise affecting the excitatory and inhibitory neurons.
    "noise_exc": [[0.07, 0.075] * nA] * copy_times,  # OLD: [0.1045, 0.104]
    "noise_inh": [[0.05, 0.08] * nA] * copy_times,

    # Defining the base probabilities of connections between neurons:
    # - p_e2e => Probability of an excitatory to excitatory neuron (synapse) connection.
    # - p_e2i => Probability of an excitatory to inhibitory neuron (synapse) connection.
    # - p_i2e => Probability of an inhibitory to excitatory neuron (synapse) connection.
    # - p_i2i => Probability of an inhibitory to inhibitory neuron (synapse) connection.
    # Normal ranges from 0.7-0.75, to activate sprouting increase the normal by 0.5
    # This will increase the average number of excitatory connections by 500.
    "p": [[0.75, 0.35, 0.35, 0.0]] * copy_times,

    # Defining the stimulus settings where with the coordinates of (300, 300, 300) the stimulus will be applied to the middle of the neuron block.
    "input_signal_file": ['sigmoid-1.0.txt'] * copy_times,
    "coord_of_stimulus": [[300, 300, 300]] * copy_times,
    "radius_of_stimulus": [180] * copy_times,

    # Defining the treatment settings.
    "device_sensitivity": [8 * ms] * copy_times,
    # Device sensitivity - how frequently to check is firing rate is above the threshold
    "firing_rate_threshold": [5 * Hz] * copy_times,
    "Eke_treatment": [-100 * mV] * copy_times,
    "Eki_treatment": [-90 * mV] * copy_times,
    "radius_of_electrode": [200] * copy_times,
    "distance_between_masks": [100] * copy_times,
}

populate_electrode_positions(variables)
