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

class IsingHamiltonian:
    def __init__(self, J=[[()]], mus=np.zeros(1)):
        self.J = J  # interactions between nodes
        self.mus = mus  # magnetic field strength for each node
        
    def energy(self, state):
        
        if len(state.config) != len(self.J):
                error("wrong dimension")
                
        e = 0.0
        state_list = list(state)
        for i in range(state.N):
            #print()
            #print(i)
            for j in self.J[i]:
                if j[0] < i:
                    continue
                #print(j)
                if state_list[i] == state_list[j[0]]:
                    e += j[1]
                else:
                    e -= j[1]
    
        e += np.dot(self.mus, 2*state.config-1)
        
        return e
        
        """if len(state.config) != len(self.J):
            #print (len(state.config))
            #print len(self.J)
            #print ("failed")
            pass
        
        e = 0.0
        state_list = list(state)

        for i in range(state.N):
            for j in self.J[i]:
                if j[0] >= i and state_list[i] == state_list[j[0]]:
                    e += j[1]
                elif j[0] >= i:
                    e -= j[1]
        for i in range(len(state)):
            e -= self.mus[i] * state_list[i]
                    
        e += np.dot(self.mus, 2*state.config-1)

        return e"""
        
    def delta_e_for_flip(self, i, state):
    
        spin = 1 - state.config[i]
        del_e = 0.0
        for j in self.J[i]:
            adjspin = state.config[j[0]]
            del_e += j[1] * (2*adjspin - 1) * (2 * spin - 1)
        del_e += 2* self.mus[i] * (spin - state.config[i])
        
        return del_e
    
    def metropolis_sweep(self, state, T=1.0):
        """Perform a single sweep through all the sites and return updated configuration
        Parameters
        ----------
        state   : list[int]
            Input state/configuration 
        T       : float
            Temperature
            
        Returns
        -------
        state   : list[int]
            Returns updated state/configuration
        """
        
        for i in range(len(state)):
            delta_e = self.delta_e_for_flip(i, state)
            
            if delta_e < 0:
                state.flip[i]
                """if state.config[i] == 0:
                    state.config[i] = 1
                else:
                    state.config[i] = 0"""
            else:
                r = random.random()
                if r < np.exp(-delta_e/T):
                    state.flip[i]
                    """if state[i] == 0:
                        state[i] = 1
                    else:
                        state[i] = 0"""
                
        return state
    
    def compute_average_values(self, state, T):
        """ Compute Average values exactly
        Parameters
        ----------
        state   : list[int]
            input state/configuration 
        T       : float
            Temperature
        
        Returns
        -------
        E       : float 
            Energy
        M       : float
            Magnetization
        HC      : float
            Heat Capacity
        MS      : float
            Magnetic Susceptability
        """
        n_sites = len(state)
        E = 0.0
        M = 0.0
        Z = 0.0
        EE = 0.0
        MM = 0.0
        
        for i in range(2**n_sites):
            spin = np.array([int(x) for x in list(np.binary_repr(i, width=n_sites))])
            spin_str = ''.join(str(x) for x in spin)
            conf = montecarlo.BitString(spin_str)
            Ei = self.energy(conf)
            Zi = np.exp(-Ei/T)
            E += Ei*Zi
            EE += Ei*Ei*Zi
            Mi = np.sum(2*spin-1)
            M += Mi*Zi
            MM += Mi*Mi*Zi
            Z += Zi
        
        E = E/Z
        M = M/Z
        EE = EE/Z
        MM = MM/Z
        
        HC = (EE - E*E)/(T*T)
        MS = (MM - M*M)/T
        
        return E, M, HC, MS