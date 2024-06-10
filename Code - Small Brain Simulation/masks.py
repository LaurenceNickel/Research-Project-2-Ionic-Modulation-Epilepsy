import numpy as np

def create_spherical_mask (topology, mask_settings):
    
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

#         distance_xy = np.sqrt((x[neuron_id] - coord_of_electrode[0])**2 + ((y[neuron_id] - coord_of_electrode[1])**2))

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