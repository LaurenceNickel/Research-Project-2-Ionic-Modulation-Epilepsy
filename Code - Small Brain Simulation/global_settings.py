from brian2 import *

# Run

integ_method='exponential_euler'

# Noise

tau_noise = 1*ms
# mu_noise_inh = 0.05*nA
# sigma_noise_inh = 0.08*nA

# mu_noise = 0.06*nA
# sigma_noise = 0.12*nA

# Equations

V_th=-20*mvolt
gM=90 * usiemens*cmetre**-2

V_th=-20*mvolt
gM=90 * usiemens*cmetre**-2
tau_Cl = 0.1 *second
pas_de_temps = 0.05*ms # defined this ourselves

taille_inh_normale=14e3 * umetre ** 2
taille_exc_normale=29e3 * umetre ** 2

glu = 1

reset_eqs='''glu=glu-0
Cl=Cl+0.2
'''

# Synapses

g_max_i = 0.6 * nsiemens
g_max_e = 60. * psiemens
gain = 1.0

# LFP

sigma = 0.3*siemens/meter # Resistivity of extracellular field (0.3-0.4 S/m)