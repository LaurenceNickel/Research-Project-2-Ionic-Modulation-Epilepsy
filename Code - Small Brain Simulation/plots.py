import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly
import plotly.express as px

def plot_neuron_map (excitatory_topolopy, inhibitory_topology):

    x_exc, y_exc, z_exc = excitatory_topolopy
    x_inh, y_inh, z_inh = inhibitory_topology

    fig = plt.figure(figsize = (10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_exc, y_exc, z_exc, c='r', marker='o', label='Excitatory')
    ax.scatter(x_inh, y_inh, z_inh, c='b', marker='o', label='Inhibitory')

    plt.legend()

    # Set labels and title
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('3D Neural Map')

    plt.plot()

def plot_connectivity (central_neuron_id, topology_home, topology_away, synapse_conn, run_id):
    
    x, y, z = topology_away
    x_home, y_home, z_home = topology_home

    coordinates = []

    indices = [index for index, value in enumerate(synapse_conn.i) if value == central_neuron_id]
    neuron_ids = [synapse_conn.j[index] for index in indices]

    for neuron_id in neuron_ids:
        if neuron_id != central_neuron_id:
            coord = [x[neuron_id], y[neuron_id], z[neuron_id]]
            coordinates.append(coord)

    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    z_coords = [coord[2] for coord in coordinates]

    mask = np.zeros(len(x_coords)+1)
    
    
    x_coords.append(x_home[central_neuron_id])
    y_coords.append(y_home[central_neuron_id])
    z_coords.append(z_home[central_neuron_id])
    mask[-1] = 1
    
    data = {
        'x': x_coords,
        'y': y_coords,
        'z': z_coords,
        'mask': mask
    }


    topology_df = pd.DataFrame(data)

    topology_df['mask'] = topology_df['mask'].replace({0: 'Connected Neurons', 1: 'Central Neuron'})

    fig = px.scatter_3d(topology_df, x='x', y='y', z='z', color='mask', 
                        color_discrete_map={"Connected Neurons": 'black', "Central Neuron": 'red'}
                       )

    fig.update_traces(marker=dict(size=4))
    
    fig.update_layout(
        scene = dict(
        xaxis = dict(nticks=5, range=[0,1000],),
                     yaxis = dict(nticks=5, range=[0,1000],),
                     zaxis = dict(nticks=5, range=[0,1000],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))

    plotly.offline.plot(fig, filename=f'./results/{run_id}/neuron-connectivity.html', auto_open=False)
#     fig.show()



def plot_neuron_mask (topology, mask, color, mask_name, run_id):
    
    data = {
        'x': topology[0],
        'y': topology[1],
        'z': topology[2],
        'mask': mask
    }


    topology_df = pd.DataFrame(data)

    topology_df['mask'] = topology_df['mask'].replace({0: 'Nearby Neurons', 1: 'Mask Affect Area'})

    fig = px.scatter_3d(topology_df, x='x', y='y', z='z', color='mask', 
                        color_discrete_map={"Nearby Neurons": 'gray',
                                           "Mask Affect Area": color}
                       )

    fig.update_traces(marker=dict(size=4))


    plotly.offline.plot(fig, filename=f'./results/{run_id}/{mask_name}-mask.html', auto_open=False)

def plot_neuron_masks (topology_exc, masks, run_id, colors=['red', 'blue']):
    
    treatment_mask_exc, stimulus_mask_exc = masks

    combined_mask = np.zeros(len(treatment_mask_exc))
    combined_mask[treatment_mask_exc == 1] = 1
    combined_mask[stimulus_mask_exc == 1] = 2


    data = {
        'x': topology_exc[0],
        'y': topology_exc[1],
        'z': topology_exc[2],
        'mask': combined_mask
    }


    topology_df = pd.DataFrame(data)

    topology_df['mask'] = topology_df['mask'].replace({0: 'Nearby Neurons', 1: 'Treatment Mask', 2: 'Stimulus Mask'})

    fig = px.scatter_3d(topology_df, x='x', y='y', z='z', color='mask', 
                        color_discrete_map={
                            "Nearby Neurons": 'gray',
                            "Stimulus Mask": colors[0],
                            "Treatment Mask": colors[1]
                                           }
                       )

    fig.update_traces(marker=dict(size=4))

    plotly.offline.plot(fig, filename=f'./results/{run_id}/neuron-masks.html', auto_open=False)
#     fig.show()