"""
Unit and regression test for the molecool package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import molecool

from molecool import *


def test_molecool_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "molecool" in sys.modules

def testa():
    assert 1 == 1
    
def test_energy():
    #state = BitString([0,0,0,0,0,0,0,0,0,0])
    state = BitString("0000000000")
    Jval = 1.0
    T = 2.0
    
    mus = [.1 for i in range(len(state))]
    J = [[(1,1),(2,1),(3,1)]]
    
    for i in range(len(state)):
        J.append([((i+1) % len(state), Jval), ((i-1) % len(state), Jval)])
    ham2 = IsingHamiltonian(J=J, mus=mus)
    e = ham2.energy(state)
    
    print (e)
    

    