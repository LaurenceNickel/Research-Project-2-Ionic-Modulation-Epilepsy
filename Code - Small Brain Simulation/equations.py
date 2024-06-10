from global_settings import *

inh_eqs = '''
    dv/dt = ( - I_leak - I_K - I_Na - I_SynE - I_SynI + I_noise) / ((1 * ufarad * cm ** -2) * (taille)) : volt 
    Vm = (- I_leak - I_K - I_Na) / ((1 * ufarad * cm ** -2) * (taille))*pas_de_temps : volt 
    I_leak = ((0.1e-3 * siemens * cm ** -2) * (taille)) * (v - (-65 * mV)) : amp 
    I_K = ((9e-3 * siemens * cm ** -2) * (taille)) * (n ** 4) * (v - ((Eki_baseline*(1-treatment_mask)) + (Eki*treatment_mask))) : amp
        dn/dt = (n_inf - n) / tau_n : 1
        n_inf = alphan / (alphan + betan) : 1
        tau_n = 0.2 / (alphan + betan) : second
        alphan = 0.01 * (mV ** -1) * (v  + 34 * mV) / (1. - exp(- 0.1 * (mV ** -1) * (v + 34 * mV))) / ms : Hz
        betan = 0.125 * exp( - (v + 44 * mV) / (80 * mV)) / ms : Hz
    I_Na = ((35e-3 * siemens * cm ** -2) * (taille)) * (m ** 3) * h * (v - (55 * mV)) : amp
        dm/dt = (m_inf - m) / tau_m : 1
        dh/dt = (h_inf - h) / tau_h : 1
        m_inf = alpham / (alpham + betam)  : 1
        tau_m = 0.2 / (alpham + betam) : second
        h_inf = alphah / (alphah + betah) : 1
        tau_h = 0.2 / (alphah + betah) : second
        alpham = 0.1 * (mV ** -1) * (v + 35 * mV) / (1. - exp(- (v + 35 * mV) / (10 * mV))) / ms : Hz
        betam = 4 * exp(- (v + 60 * mV) / (18 * mV)) / ms : Hz
        alphah = 0.07 * exp(- (v + 58 * mV) / (20 * mV)) / ms : Hz
        betah = 1. / (exp((- 0.1 * (mV ** -1)) * (v + 28 * mV)) + 1.) / ms : Hz
    I_SynE = + ge * (v - (0 * mV)) : amp
        dge/dt = (-ge+he) * (1. / (0.3 * ms)) : siemens
        dhe/dt=-he/(5*ms) : siemens
    I_SynI = + gi * (v - (-80 * mV)) : amp
        dgi/dt = (-gi+hi) * (1. / (1 * ms)) : siemens
        dhi/dt=-hi/(10*ms) : siemens
        
    x:metre
    y:metre
    z:metre
    treatment_mask:1
    taille:metre ** 2
    
    dI_noise/dt = (mu_noise - I_noise)/tau_noise + noise : amp
    noise = sigma_noise*sqrt(2/tau_noise)*randn()/sqrt(dt) : amp/second (constant over dt)

    sigma_noise : amp
    mu_noise : amp

    '''

py_eqs = '''
    dv/dt = ( - I_M - I_leak - I_K - I_Na - I_Ca - I_SynE - I_SynI + I_stim + I_noise) / ((1 * ufarad * cm ** -2) * (taille)) : volt 
    Vm=( - I_M - I_leak - I_K - I_Na - I_Ca) / ((1 * ufarad * cm ** -2) * (taille))*pas_de_temps : volt 
    Im = (I_leak + I_K + I_Na + I_Ca) / (29e3 * um ** 2) : amp/meter**2
    I_M = ((gM) * (taille)) * p * (v - ((Eke_baseline*(1-treatment_mask)) + (Eke*treatment_mask))) : amp
        dp/dt = (pInf - p) / pTau : 1
        pInf = 1. / (1 + exp(- (v + (35 * mV)) / (10 * mV))) : 1
        pTau = (1000 * ms) / (3.3 * exp((v + (35 * mV)) / (20 * mV)) + exp(- (v + (35 * mV)) / (20 * mV))) : second
    I_leak = ((1e-5 * siemens * cm ** -2) * (taille)) * (v - (-70*mV)) : amp 
    I_K = ((5 * msiemens * cm ** -2) * (taille)) * (n ** 4) * (v - ((Eke_baseline*(1-treatment_mask)) + (Eke*treatment_mask))) : amp
        dn/dt = alphan * (1 - n) - betan * n : 1
        alphan =  - 0.032 * (mV ** -1) * (v  - (-55 * mV) - 15 * mV) / (exp(- (v - (-55 * mV) - 15 * mV) / (5 * mV)) - 1.) / ms : Hz
        betan = 0.5 * exp( - (v - (-55 * mV) - 10 * mV) / (40 * mV)) / ms : Hz
    I_Na = ((50 * msiemens * cm ** -2) * (taille)) * (m ** 3) * h * (v - (50 * mV)) : amp
        dm/dt = alpham * (1 - m) - betam * m : 1
        dh/dt = alphah * (1 - h) - betah * h : 1
        alpham = - 0.32 * (mV ** -1) * (v - (-55 * mV) - 13 * mV) / (exp(- (v - (-55 * mV) - 13 * mV) / (4 * mV)) - 1.) / ms : Hz
        betam = 0.28 * (mV ** -1) * (v - (-55 * mV) - 40 * mV) / (exp((v - (-55 * mV) - 40 * mV) / (5 * mV)) - 1.) / ms : Hz
        alphah = 0.128 * exp(- (v - (-55 * mV) - 17 * mV) / (18 * mV)) / ms : Hz
        betah = 4. / (1 + exp(- (v - (-55 * mV) - 40 * mV) / (5 * mV))) / ms : Hz
    I_Ca = ((1e-4 * siemens * cm ** -2) * (taille)) * (mCaL ** 2) * hCaL * (v - (120 * mV)) : amp
        dmCaL/dt = (alphamCaL * (1 - mCaL)) - (betamCaL * mCaL) : 1
        dhCaL/dt = (alphahCaL * (1 - hCaL)) - (betahCaL * hCaL) : 1
        alphamCaL = (0.055 * mV ** -1) * ((-27 * mV) - v) / (exp(((-27 * mV) - v) / (3.8 * mV)) - 1.) / ms : Hz
        betamCaL = 0.94 * exp(((-75 * mV) - v) / (17 * mV)) / ms : Hz
        alphahCaL = 0.000457 * exp(((-13 * mV) - v) / (50 * mV)) / ms : Hz
        betahCaL = 0.0065 / (exp(((-15 * mV) - v) / (28 * mV)) + 1.) / ms : Hz
        dCa_i/dt = driveChannel + ((2.4e-4 * mole * metre**-3) - Ca_i) /  (200 * ms) : mole * meter**-3
        driveChannel = (-(1e4) * I_Ca / (cm ** 2)) / (2 * (96489 * coulomb * mole ** -1) * (1 * umetre)) : mole * meter ** -3 * Hz

    I_SynE = + ge * (v - (0 * mV)) : amp
        dge/dt = (-ge+he) * (1. / (0.3 * ms)) : siemens
        dhe/dt=-he/(5*ms) : siemens
    I_SynI = + gi*(v - (-50 * mV))*int(Cl>0.5) + gi*(v - (-80 * mV))*int(Cl<=0.5): amp
        dgi/dt = (-gi+hi) * (1. / (1 * ms)) : siemens
        dhi/dt=-hi/(10*ms) : siemens   
        
    dCl/dt=-Cl/tau_Cl:1          

        
    dglu/dt=(1-glu)/(3*second):1  
    
    x:metre
    y:metre
    z:metre
    x_dendrite:metre
    y_dendrite:metre
    z_dendrite:metre
    x_inh:metre
    y_inh:metre
    z_inh:metre
    dir_x:1
    dir_y:1
    dir_z:1
    treatment_mask:1
    stimulus_mask:1
    taille:metre ** 2

    I_stim = input_signal(t)*stimulus_mask : amp
    
    dI_noise/dt = (mu_noise - I_noise)/tau_noise + noise : amp
    noise = sigma_noise*sqrt(2/tau_noise)*randn()/sqrt(dt) : amp/second (constant over dt)

    sigma_noise : amp
    mu_noise : amp

    ''' 