import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly
import plotly.express as px
import plotly.graph_objects as go


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


# Plotting all the hippocampal topologies in single 3D plot.
def plot_all_hippocampal_topologies(topologies, topology_names, run_id):

    # Initializing a figure.
    fig = go.Figure()

    # Defining the colors of the different hippocampal regions.
    colors = ['red', 'blue', 'green', 'purple']

    # Defining the shapes of the different types of neurons.
    shapes = {'excitatory': 'circle', 'inhibitory': 'square'}
    
    # Determining the number of topology pairs.
    num_pairs = len(topologies) // 2
    
    # Looping over all the topology pairs.
    for i in range(num_pairs):
        
        # Extracting the excitatory and inhibitory topology for the same region.
        topology_exc = topologies[i]
        topology_inh = topologies[i + num_pairs]
        
        # Unpacking the topology data.
        x_exc, y_exc, z_exc = topology_exc
        x_inh, y_inh, z_inh = topology_inh
        
        # Creating excitatory and inhibitory DataFrames with the topology data.
        data_exc = {
            'x': x_exc,
            'y': y_exc,
            'z': z_exc,
            'type': 'excitatory'}
        df_exc = pd.DataFrame(data_exc)
        data_inh = {
            'x': x_inh,
            'y': y_inh,
            'z': z_inh,
            'type': 'inhibitory'}
        df_inh = pd.DataFrame(data_inh)
        
        # Plotting the excitatory data.
        fig.add_trace(go.Scatter3d(
            x=df_exc['x'],
            y=df_exc['y'],
            z=df_exc['z'],
            mode='markers',
            marker=dict(size=4, color=colors[i], symbol=shapes['excitatory']),
            name=topology_names[i]
        ))

        # Plotting the inhibitory data.
        fig.add_trace(go.Scatter3d(
            x=df_inh['x'],
            y=df_inh['y'],
            z=df_inh['z'],
            mode='markers',
            marker=dict(size=4, color=colors[i], symbol=shapes['inhibitory']),
            name=topology_names[i+num_pairs]
        ))
    
    # Setting labels for the axes.
    fig.update_layout(scene=dict(
        xaxis_title='X axis',
        yaxis_title='Y axis',
        zaxis_title='Z axis'
    ))
    
    # Saving the plot as an HTML file.
    plotly.offline.plot(fig, filename=f'./results/{run_id}/all_hippocampal_topologies.html', auto_open=False)


# Plotting the stimulus and treatment masks in a single 3D plot featuring all the hippocampal topologies.
def plotting_masks(topologies, topology_names, topology_featuring_masks, masks, run_id):

    # Initializing a figure and setting the default color of the points.
    fig = go.Figure()
    default_color = 'rgba(0, 0, 255, 0.2)'

    # Extracting the stimulus mask as well as which topology features the mask and what the color of the corresponding points in the 3D plot should be.
    stimulus_mask = masks[0]
    stimulus_topology_featuring_mask = topology_featuring_masks[0][0]
    stimulus_color = 'red'

    # Extracting the treatment masks as well as which topologies feature the masks and what the color of the corresponding points in the 3D plot should be.
    treatment_mask_exc, treatment_mask_inh = masks[1]
    treatment_topology_featuring_mask_exc, treatment_topology_featuring_mask_inh = topology_featuring_masks[1]
    treatment_color = 'yellow'

    # Iterating over the topologies.
    for i, (topology, topology_name) in enumerate(zip(topologies, topology_names)):
        
        # Unpacking the coordinates of the topology.
        x, y, z = topology
        
        # Creating a list to store the color of each neuron and initializing it with the defined default color.
        colors = [default_color] * len(x)
        
        # Highlighting the neurons in the current topology that are part of the stimulus mask.
        if topology_name == stimulus_topology_featuring_mask:
            for j, is_in_mask in enumerate(stimulus_mask):
                if is_in_mask == 1:
                    colors[j] = stimulus_color

        # Highlighting the neurons in the current topology that are part of the excitatory treatment mask.
        if topology_name == treatment_topology_featuring_mask_exc:
            for j, is_in_mask in enumerate(treatment_mask_exc):
                if is_in_mask == 1:
                    colors[j] = treatment_color
                    
        # Highlighting the neurons in the current topology that are part of the inhibitory treatment mask.
        if topology_name == treatment_topology_featuring_mask_inh:
            for j, is_in_mask in enumerate(treatment_mask_inh):
                if is_in_mask == 1:
                    colors[j] = treatment_color

        # Plotting the data while taking into account the defined 'colors' list.
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(size=4, color=colors),
            name=topology_name
        ))

    # Setting the labels of the axes.
    fig.update_layout(scene=dict(
        xaxis_title='X axis',
        yaxis_title='Y axis',
        zaxis_title='Z axis'
    ))

    # Saving the 3D plot as an HTML file.
    plotly.offline.plot(fig, filename=f'./results/{run_id}/all_hippocampal_topologies_with_masks.html', auto_open=False)
                

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