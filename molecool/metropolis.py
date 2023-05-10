#import montecarlo
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy as cp

#returns new avg after considering all prev ones and curr one.
def run_avg(prev, curr, i):
    return (prev*(i-1)+curr)/i

def metropolis_montecarlo(ham, state, T=1, nsweep=1000, nburn=100):
    
    ham.metropolis_sweep(state, T=T)
    Ei = ham.energy(state)
    Mi = state.get_mag()
    E_list = [Ei]
    M_list = [Mi] 
    EE_list = [Ei**2]
    MM_list = [Mi**2]  
    # run metropolis sweep on initial state to populate array
    #for loop through all possible flips and append the cumilitive 
    #parameters to the array
    for i in range(2,nsweep+1):
        ham.metropolis_sweep(state, T=T)
        Ei = ham.energy(state)
        Mi = state.get_mag()
        
        E_list.append(run_avg(E_list[-1], Ei, i))
        M_list.append(run_avg(M_list[-1], Mi, i))
        EE_list.append(run_avg(EE_list[-1], Ei ** 2, i))
        MM_list.append(run_avg(MM_list[-1], Mi ** 2, i))

    return E_list, M_list, EE_list, MM_list

