
import numpy as np
from brian2 import *
import random
import os

from helper import *
from masks import *

def run_model_loop (variables):

    if not check_dict_lenghts(variables):
        raise ValueError('Lenghts of each variable list has be to equal!')

    variables["coord_of_electrode"] = populate_electrode_positions(variables)

    for i in range(len(variables['run_id'])):
        
        start_scope()
        defaultclock.dt = 0.001*second   

        current_variables = {key: variables[key][i] for key in variables}

        # Create folder
        run_id = current_variables["run_id"]
        os.mkdir(f'./results/{run_id}')
        write_run_settings(current_variables, run_id)
        
        # Noise
        mu_noise_inh = current_variables['noise_inh'][0]
        sigma_noise_inh = current_variables['noise_inh'][1]

        mu_noise = current_variables['noise_exc'][0]
        sigma_noise = current_variables['noise_exc'][1]

        # Create dynamic objects based on variables provided
        topology_exc = create_neuron_topology(current_variables['N'][0], current_variables['bounds'])
        topology_inh = create_neuron_topology(current_variables['N'][1], current_variables['bounds'])
        topologies = [topology_exc, topology_inh]
        
        stimulus_geometry_settings = [current_variables['coord_of_stimulus'], current_variables['radius_of_stimulus']]
        stimulus_mask_exc = create_spherical_mask(topology_exc, stimulus_geometry_settings)
        
        treatment_geometry_settings = [current_variables['coord_of_electrode'], current_variables['radius_of_electrode']]
        treatment_mask_exc = create_spherical_mask(topology_exc, treatment_geometry_settings)
        treatment_mask_inh = create_spherical_mask(topology_inh, treatment_geometry_settings)
        treatment_masks = [treatment_mask_exc, treatment_mask_inh]
        
        treatment_settings = [current_variables['device_sensitivity'], current_variables['firing_rate_threshold']]
        
        # Instantiate the Network
        net, synapses, monitors = prepare_network(topologies, stimulus_mask_exc, treatment_masks, current_variables['p'])
        popmon_exc, popmon_inh, statemon_exc, statemon_inh, Mlfp = monitors
        
        # Write network statistics
        write_network_statistics(synapses, current_variables['N'])

        # Save network plots
        # plot_neuron_masks (topology_exc, [stimulus_mask_exc, treatment_mask_exc], run_id)
        plot_neuron_mask (topology_exc, stimulus_mask_exc, 'red', 'stimulus', run_id)
        plot_neuron_mask (topology_exc, treatment_mask_exc, 'blue', 'treatment', run_id)

        # Run the simulation
        run_granular_simulation (current_variables, treatment_settings, monitors)
        
        # Save Firing Rate Data
        np.savetxt(f'./results/{run_id}/fr_exc.txt', popmon_exc.rate)
        np.savetxt(f'./results/{run_id}/fr_inh.txt', popmon_inh.rate)
        
        #Plot the Firing Rate and Noise
        
        plt.plot(popmon_inh.t, popmon_inh.rate, label='Inhibitory')
        plt.plot(popmon_exc.t, popmon_exc.rate, label='Excitatory')

        plt.legend()
        plt.savefig(f'./results/{run_id}/firing-rates.png', bbox_inches='tight')
        plt.close()
        
        plt.plot(statemon_inh.t, statemon_inh.I_noise[4]/nA, label='inh')
        plt.savefig(f'./results/{run_id}/noise_inh.png', bbox_inches='tight')
        plt.close()
        
        plt.plot(statemon_exc.t, statemon_exc.I_noise[4]/nA, label='exc')
        plt.savefig(f'./results/{run_id}/noise_exc.png', bbox_inches='tight')
        plt.close()
        
        np.savetxt(f'./results/{run_id}/LFP.txt', Mlfp.v[0]/mV)
        plot(Mlfp.t/ms, Mlfp.v[0]/mV)
        plt.savefig(f'./results/{run_id}/LFP.png', bbox_inches='tight')
        plt.close()
        