#import montecarlo
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy as cp

def metropolis_montecarlo(ham, state, T=1, nsweep=1000, nburn=100):
    E_samples = np.zeros(nsweep) 
    M_samples = np.zeros(nsweep) 
    EE_samples = np.zeros(nsweep) 
    MM_samples = np.zeros(nsweep) 
    
    # thermalization
    for si in range(nburn):
        ham.metropolis_sweep(state, T=T)
    
    # accumulation
    ham.metropolis_sweep(state, T=T)
    Ei = ham.energy(state)
    Mi = state.get_mag()
    M_samples[0]  = Mi 
    E_samples[0]  = Ei
    MM_samples[0]  = Mi*Mi 
    EE_samples[0]  = Ei*Ei
    for si in range(1,nsweep):
        ham.metropolis_sweep(state, T=T)
        Ei = ham.energy(state)
        Mi = state.get_mag()
        
        E_samples[si]  = (E_samples[si-1]*(si) + Ei)/(si+1)
        EE_samples[si] = (EE_samples[si-1]*(si) + Ei*Ei)/(si+1)
        
        M_samples[si]  = (M_samples[si-1]*(si) + Mi)/(si+1)
        MM_samples[si] = (MM_samples[si-1]*(si) + Mi*Mi)/(si+1)

    return E_samples, M_samples, EE_samples, MM_samples