import numpy as np

def check_dict_lenghts (variables):
    flag = 0
    lens = map(len, variables.values())
    if len(set(lens)) == 1:
        flag = 1
        
    return flag

def write_run_settings (run_dict, run_id):
    with open(f"./results/{run_id}/settings.txt", "w") as f:
        for key, value in run_dict.items():  
            f.write('%s: %s\n' % (key, value))

def connection_statistics (synpase, N):
    
    nos, _ = np.histogram(synpase.i, bins=np.arange(0, len(synpase.source), 1))
    probarray = nos / len(synpase.target)
    avg_probability = np.mean(probarray)


    return avg_probability, len(synpase.i) / N

def write_network_statistics(synapses, Ns, run_id):
    avg_connection_probability, avg_num_connections = connection_statistics(synapses[0], Ns[0]) 
    avg_connection_probability2, avg_num_connections2 = connection_statistics(synapses[1], Ns[0]) 
    avg_connection_probability3, avg_num_connections3 = connection_statistics(synapses[2], Ns[1]) 

    with open(f"./results/{run_id}/network_statistics.txt", "w") as f:
        f.write('Statistics for e2e\n')
        f.write(f'Average Connection Probability: {str(avg_connection_probability)}%\n')
        f.write(f'Average Number of Connections: {str(avg_num_connections)}\n\n')
        
        f.write('Statistics for e2i\n')
        f.write(f'Average Connection Probability: {str(avg_connection_probability2)}%\n')
        f.write(f'Average Number of Connections: {str(avg_num_connections2)}\n\n')
    
        f.write('Statistics for i2e\n')
        f.write(f'Average Connection Probability: {str(avg_connection_probability3)}%\n')
        f.write(f'Average Number of Connections: {str(avg_num_connections3)}\n\n')