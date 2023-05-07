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

    ham.metropolis_sweep(state, T=T)

    for i in range(nsweep):
        Ei = ham.energy(state)
        Mi = np.sum(2*state-1)
        M_samples[0] = Mi
        E_samples[0] = Ei
        MM_samples[0] = Mi**2
        EE_samples[0] = Ei**2

    E_samples = np.cumsum(E_samples) / (np.arange(nsweep) + 1)
    M_samples = np.cumsum(M_samples) / (np.arange(nsweep) + 1)
    
    HC = (np.sum(EE_samples) / nsweep - (np.sum(E_samples) / nsweep)**2) / (T**2)
    MS = (np.sum(MM_samples) / nsweep - (np.sum(M_samples) / nsweep)**2) / T
    
    return E_samples, M_samples, HC, MS