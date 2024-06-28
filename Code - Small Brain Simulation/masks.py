import numpy as np
from brian2 import *


# Creating a spherical mask based on the passed on topology and mask settings.
def create_spherical_mask(topology, mask_settings):
    
    # Retrieving the x-coordinates, y-coordinates, and z-coordinates from the neurons present in the 'topology' and the coordinates and radius from the 'mask_settings'.
    x, y, z = topology
    coord_of_mask, radius_of_mask = mask_settings

    # Initializing a variable that will contain for each neuron whether it is in the spherical mask or not.
    mask = np.zeros(len(x))

    # Looping over every neuron in the 'topology', calculating its distance from the coordinates of the mask and evaluating whether it is smaller than the radius.
    for neuron_id in range(len(x)):
        distance_xyz = np.sqrt((x[neuron_id] - coord_of_mask[0])**2 + ((y[neuron_id] - coord_of_mask[1])**2) + ((z[neuron_id] - coord_of_mask[2])**2))
        mask[neuron_id] = (distance_xyz <= radius_of_mask)

    return mask


# Creating a cubical mask based on the passed on topology and mask settings.
def create_cubical_mask(topology, mask_settings):
    
    # Retrieving the x-coordinates, y-coordinates, and z-coordinates from the neurons present in the 'topology' and the coordinates and edge length from the 'mask_settings'.
    x, y, z = topology
    coord_of_mask, edge_length_mask = mask_settings

    # Initializing a variable that will contain for each neuron whether it is in the cubical mask or not.
    mask = np.zeros(len(x))

    # Looping over every neuron in the 'topology', calculating its distance from the coordinates of the mask and evaluating whether it is smaller than half the edge length.
    for neuron_id in range(len(x)):
        within_x = abs(x[neuron_id] - coord_of_mask[0]) <= (edge_length_mask / 2)
        within_y = abs(y[neuron_id] - coord_of_mask[1]) <= (edge_length_mask / 2)
        within_z = abs(z[neuron_id] - coord_of_mask[2]) <= (edge_length_mask / 2)
        mask[neuron_id] = within_x and within_y and within_z

    return mask


# Creating a mask that will feature all neurons in the passed on topology.
def create_all_mask(topology):
    
    # Retrieving the x-coordinates, y-coordinates, and z-coordinates from the neurons present in the 'topology'.
    x, y, z = topology

    # Initializing a variable with all ones such that every neuron in the 'topology' is included in the mask.
    mask = np.ones(len(x))

    return mask


# Creating a mask that will feature a percentage of all the neurons in the passed on topology.
def create_prec_of_all_mask(topology, percentage):
    
    # Retrieving the x-coordinates, y-coordinates, and z-coordinates from the neurons present in the 'topology'.
    x, y, z = topology

    # Randomly generating a list of neuron ids based on the passed on 'percentage'.
    num_of_neurons_to_include = int((len(x) * percentage) / 100)
    neuron_sequence = np.random.choice(len(x), num_of_neurons_to_include, replace=False)

    # Initializing a variable that will contain for each neuron whether it is in the mask or not.
    mask = np.zeros(len(x))

    # Looping over every neuron in the 'topology' and setting its value to 1 if it was included in the 'neuron_sequence' list.
    for neuron_id in range(len(x)):
        if neuron_id in neuron_sequence:
            mask[neuron_id] = 1
            
    return mask



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