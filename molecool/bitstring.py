import numpy as np
from numpy.testing import assert_almost_equal
import random
import copy as cp

class BitString:
    """
    Simple class to implement a string of bits
    """
    def __init__(self, str):
        self.string = str
        self.config = np.zeros(len(str), dtype=int)
        for i in range(len(str)):
            self.config[i] = str[i]
        self.N = len(self.config)
        #self.config = np.zeros(N, dtype = int)
        
    def __str__(self):
        tempstr = ""
        for c in self.string:
            tempstr = tempstr + str(c)
        return f"{tempstr}"
    
    def __len__(self):
        return len(self.string)
    
    def __iter__(self):
        return iter(self.config)
    
    def __eq__(self, other):
        if int(self.int()) == int(other.int()):
            return True
        return False
    
    def magInit(self, M=0, verbose=0):
        self.config = np.zeros(len(self), dtype=int)
        randomlist = random.sample(range(0, len(self)),M)
        for i in randomlist:
            self.config[i] = 1
            
    def get_mag(self):
        return np.sum(2*self.config-1)
    
    def get_str(self):
        return self.string
    
    def flip(self, i):
        if self.config[i] == 1:
            self.config[i] = 0
        else:
            self.config[i] = 1

    def set_string(self, list):
        tempstr = ""
        for bit in list:
            tempstr = tempstr + str(bit)
        self.string = tempstr
        #self.config = np.zeros(len(str), dtype=int)
        for i in range(len(tempstr)):
            self.config[i] = tempstr[i]
        self.N = len(self.config)

    def on(self):
        onct = 0;
        for bit in self.string:
            if bit == '1':
                onct+=1
        return onct
    
    def off(self):
        offct = 0;
        for bit in self.string:
            if bit == '0':
                offct+=1
        return offct
    
    def int(self):
        tempstr = ""
        for c in self.string:
            tempstr = tempstr + str(c)
        binInt = int(tempstr)
        decVal, i = 0, 0
        while(binInt != 0):
            temp = binInt % 10
            decVal = decVal + temp * pow(2, i)
            binInt = binInt//10
            i += 1
        return decVal
    
    def set_int(self, val):
        num_bits = int(np.log2(val)) + 1
        bin_str = np.binary_repr(val, width=len(self.config))
        self.string = bin_str
        for i in range(len(self.config)):
            self.config[i] = bin_str[i]
        print (self.string)
        print (self.config)
        """print (self.string)
        self.string = ""
        self.recurseSolve(val, digits)
        tempstr = self.string
        print (tempstr)
        self.string = []
        for c in tempstr:
            self.string.append(int(c))
        
        tempstr = self.string
        for i in range(len(tempstr)):
            self.config[i] = 0
        print (self.config)
        for i in range(len(tempstr)):
            self.config[i] = tempstr[i]
        print (self.config)
        self.N = len(self.config)"""
        
    def recurseSolve(self, val, digits):
        if val >= 1:
            bin = str(val%2)
            self.string = bin + self.string
            self.recurseSolve(val//2, digits-1)
            if len(self.string) < digits:
                self.string = '0'*(digits - len(self.string)) + self.string
        else:
            return 