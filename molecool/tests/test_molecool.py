"""
Unit and regression test for the molecool package.
"""

# Import package, test suite, and other packages as needed
import sys
import random
import pytest
import molecool as montecarlo
import numpy as np
from molecool import *



def test_molecool_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "molecool" in sys.modules

def testa():
    assert 1 == 1
    
def test_energy():
    #state = BitString([0,0,0,0,0,0,0,0,0,0])
    state = BitString("0000010000")
    Jval = 1.0
    T = 2.0
    
    mus = [.1 for i in range(len(state))]
    J = [[(1,1),(2,1),(3,1)]]
    
    for i in range(len(state)):
        J.append([((i+1) % len(state), Jval), ((i-1) % len(state), Jval)])
    ham2 = IsingHamiltonian(J=J, mus=mus)
    e = ham2.energy(state)
    
    assert(e == 3.2)
    
    #print (e)
    
def test_avg_val():
    #state = BitString([0,0,0,0,0,0,0,0,0,0])
    state = BitString("0000000000")
    Jval = 1.0
    T = 2.0
    
    mus = [.1 for i in range(len(state))]
    J = [[(1,1),(2,1),(3,1)]]
    
    for i in range(len(state)):
        J.append([((i+1) % len(state), Jval), ((i-1) % len(state), Jval)])
    ham2 = montecarlo.IsingHamiltonian(J=J, mus=mus)
    E, M, HC, MS = ham2.compute_average_values(state, T) 

    assert(E == -1.883414219754846)
    assert(M == -0.3806002429533456)
    assert(HC == 0.8008947941870221)
    assert(MS == 3.801275405473561)
    
def test_delta_e():
    random.seed(1)
    state = BitString("0000010000")
    Jval = 1.0
    #state.magInit(M=10)
    T = 2.0
    
    mus = [.1 for i in range(len(state))]
    J = [[(1,1),(2,1),(3,1)]]
    
    for i in range(len(state)):
        J.append([((i+1) % len(state), Jval), ((i-1) % len(state), Jval)])
    ham = IsingHamiltonian(J=J, mus=mus)
    e1 = ham.energy(state)
    
    assert(e1 == 3.2)

    e1 = ham.energy(state)
    print(" Energy = ", e1)

    delta_e1 = ham.delta_e_for_flip(5, state)
    
    state.flip(5)
    #print(conf.config)
    e2 = ham.energy(state)
    print(state)
    print(" Energy = ", e2)

    print(" delta E: %12.8f" %(e2-e1))
    print(" delta E: %12.8f" %(delta_e1))

    assert(np.isclose(e2-e1, delta_e1))
    
def test_metropolis():
    
    random.seed(2)
    state = BitString("0000010000")
    Jval = 1.0
    #state.magInit(M=10)
    T = 2.0
    
    mus = [.1 for i in range(len(state))]
    J = [[(1,1),(2,1),(3,1)]]
    
    for i in range(len(state)):
        J.append([((i+1) % len(state), Jval), ((i-1) % len(state), Jval)])
    ham = IsingHamiltonian(J=J, mus=mus)

    conf = montecarlo.BitString("0000010000")
    E, M, EE, MM = montecarlo.metropolis_montecarlo(ham, conf, T=T, nsweep=8000, nburn=1000)

    assert(np.isclose(1.75949, E[-1]))
    
    
    

    