from cmath import tan
from lib2to3.pygram import Symbols
from sympy import symbols, Eq, solve
import numpy as np
import pandas as pd
from Shifting_calcs import *
''' 
- datum is usually the fixed sheave
- outwards displacement is taken as positive (thus secondary velocities and accelerations are negative)
- outwards forces are negative 
'''
torque= 14.5        #lbf-ft

#primary data
flyweight= 420      #grams!
k1= 50              #primary linear spring rate (lb-in)

#secondary data
k2= 21              #secondary linear spring rate (lb-in)
k2_ang= 46          #secondart angular spring rate (lb-in/rad)
ramp_radius= 1.625  #inches (maybe)

#General functions
def springforce(k, disp):
    return k*disp



#Primary


#Secondary shit
'''
Force balance:
F_Net= F_belt - F_spring_angular -F_spring_linear - F_cam

Note that displacement is also resisted linearly by the angular spring
'''
def sideforce(ratio, alpha):
    return 6*torque*ratio/(ramp_radius*tan(alpha))
 
