#from numba import jit

import numpy as np
#from numpy.testing import assert_almost_equal
import random
import copy as cp
import molecool as montecarlo
from operator import itemgetter
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy
random.seed(2)
import math

#ising hamiltonian class
#takes in and initialized J and mus which are a list of the bounding forces among nodes and the magnetic forces
class IsingHamiltonian:
    def __init__(self, J=[[()]], mus=np.zeros(1)):
        self.J = J  # interactions between nodes
        self.mus = mus  # magnetic field strength for each node
        
    #energy function
    #computes the energy of a state
    #the state is a bitstring
    #adds 1 for adjacent similar states and subtracts 1 for non similar
    def energy(self, state):
                
        e = 0.0
        state_list = list(state)
        for i in range(state.N):
            #print()
            #print(i)
            for j in self.J[i]:
                if j[0] > i:
                    if state_list[i] != state_list[j[0]]:
                        e -= j[1]
                    else:
                        e += j[1]
                #print(j)
    
        dot_product = np.inner(self.mus, 2*state.config-1)
        e += dot_product
        
        return e
        
    #computes the change in the energy after one of the values in the state is flipped
    #example if i = 1, 000 becomes 010
    def delta_e_for_flip(self, i, state):
    
        """spin = 1 - state.config[i]
        del_e = 0.0
        for j in self.J[i]:
            adjspin = state.config[j[0]]
            del_e += j[1] * (2*adjspin - 1) * (2 * spin - 1)
        del_e += 2* self.mus[i] * (spin - state.config[i])
        
        return del_e"""
        del_e = 0.0
    
        spin = 1 - state.config[i]
        
        if state.config[i] == 1:
            for j in self.J[i]:
                adjspin = state.config[j[0]]
                del_e += (2.0 * adjspin - 1.0) * j[1] * -2
            del_e += self.mus[i] * -2
        else:
            for j in self.J[i]:
                adjspin = state.config[j[0]]
                del_e += (2.0 * adjspin - 1.0) * j[1] * 2
            del_e += self.mus[i] * 2
                    
        return del_e
    
    #this is used to compute the expected state after a sweep is performed
    #use the delta e to flip a state and then compute using the constants
    def metropolis_sweep(self, state, T=1.0):
        
        for i in range(len(state)):
            delta_e = self.delta_e_for_flip(i, state)
            
            if delta_e < 0:
                state.config[i] = 1 - state.config[i]
                """if state.config[i] == 0:
                    state.config[i] = 1
                else:
                    state.config[i] = 0"""
            else:
                r = random.random()
                if r < np.exp(-delta_e/T):
                    state.config[i] = 1 - state.config[i]
                    """if state[i] == 0:
                        state[i] = 1
                    else:
                        state[i] = 0"""
                
        return state
    
    #compute the average values of the config.
    def compute_average_values(self, state, T):

        n_sites = len(state)
        E = 0.0
        M = 0.0
        Bi = 0.0
        EE = 0.0
        MM = 0.0
        
        for i in range(2**n_sites):
            spin = np.array([int(x) for x in list(np.binary_repr(i, width=n_sites))])
            spin_str = ''.join(str(x) for x in spin)
            conf = montecarlo.BitString(spin_str)
            Ei = self.energy(conf)
            
            B = np.exp(-Ei/T)
            #print(B)
            
            E += Ei*B
            EE += Ei**2*B
            Mi = np.sum(2*spin-1)
            M += Mi*B
            MM += Mi**2*B
            Bi += B
        
        E /= Bi
        M /= Bi
        EE /= Bi
        MM /= Bi
        
        HC = (EE/(T**2) - E**2/(T**2))
        MS = (MM/T - M**2/T)
        
        return E, M, HC, MS