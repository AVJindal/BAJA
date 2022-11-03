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
torque= 14.5             #lbf-ft

#primary data
ramp_angle = 8           #ramp angle 
flyweight= 420           #grams!
k1= 50                   #primary linear spring rate (lb-in)
r_1= 2.5663              #dummy variable for the distance of hte ramps from the shaft centre

#secondary data
k2= 21                   #secondary linear spring rate (lb-in)
k2_ang= 46               #secondart angular spring rate (lb-in/rad)
helix_radius= 1.625       #inches
helix_angle = 22.5547      #degrees       

#General functions
def springforce(k, disp):
    return k*disp                   #disp will need to be displacement from initial position


#Primary
'''
Force Balance: 
F_Net = F_belt + F_spring - F_flyweights
'''
def flyweight_force(disp, omega=3200, theta=ramp_angle, mass=flyweight):                  #returns the force applied by the flyweights on the moving sheave
    r= r_1 + disp*np.cos(theta*np.pi/180)                                                  
    return mass*(omega**2)*r*tan((90-theta)*np.pi/180)
primary_disp = 0
def prim_balance(k=k1, d=primary_disp):
    F_s = springforce(k, d)
    F_FW = flyweight_force(d)
    return (belt_force+ F_s + F_FW)/p_move_mass

prim_max_disp = 0.684791525761340
theta_1 = 62
theta_2 = 72
flatLen = 0.23
rampLen = prim_max_disp + 0.5

x_n = 0
y_n = 0
y_ramp = []
x_ramp = []
n = 100
theta_0 = 62
incLen = rampLen/n

for c in range(n):
    x_n = x_n + incLen*np.sin(theta_0*np.pi/180)
    x_ramp.append(x_n)
    y_n = y_n + incLen*np.cos(theta_0*np.pi/180)
    y_ramp.append(y_n)
    theta_0 = theta_0 - (theta_2 - theta_1)/n
    
    # print(theta_0)

print(x_n)
print(y_n)
plt.plot(y_ramp, x_ramp)
plt.show()
# def primary_ramp_pos(mass, sheave_disp):


#Secondary 
'''
Force balance:
F_Net= F_belt - F_spring_angular -F_spring_linear - F_cam
Note that displacement is also resisted linearly by the angular spring
''' 

def sideforce(ratio, alpha):
    return 6*torque*ratio/(helix_radius*tan(alpha))

def torsion(disp, alpha=helix_angle, r=helix_radius):
    l= disp/tan(alpha*np.pi/180)
    return (k2_ang * l * 180 )/(np.pi*r**2)




