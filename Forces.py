from cmath import tan
from lib2to3.pygram import Symbols
from sympy import symbols, Eq, solve
import numpy as np
import pandas as pd
from Shifting_calcs import *
import Shifting_calcs
''' 
- datum is usually the fixed sheave
- outwards displacement is taken as positive (thus secondary velocities and accelerations are negative)
- outwards forces are negative 
'''
torque= 14.5             #lbf-ft

#primary data
flyweight= 420           #grams!
k1= 50                   #primary linear spring rate (lb-in)
r_1= 2.5663              #dummy variable for the distance of hte ramps from the shaft centre

# primary ramp initiation
prim_max_disp = 0.684791525761340
theta_1 = 62
theta_2 = 72
flatLen = 0.23
rampLen = prim_max_disp + 0.5


y_ramp = []
x_ramp = []

n = 100
theta_0 = 62
theta = [theta_0]
incLen = rampLen/n
flatX = 0.2565
flatY = 0.103
centerRampOffsetY = 2.42 #(in)
x_n = 0
y_n = centerRampOffsetY
for c in range(n):
    x_n = x_n + incLen*np.sin(theta_0*np.pi/180)
    x_ramp.append(x_n)
    y_n = y_n + incLen*np.cos(theta_0*np.pi/180)
    y_ramp.append(y_n)
    theta_0 = theta_0 + (theta_2 - theta_1)/n
    theta.append(theta_0)
    # print(theta_0)

plt.plot(y_ramp, x_ramp)
plt.show()



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
def flyweight_force(disp, omega=3200, mass=flyweight):                  #returns the force applied by the flyweights on the moving sheave
    r= primary_ramp_pos(disp)[0]/12                                     # primary_ramp_pos returns (x, y, theta) converts in to ft 
    omega = omega*((2*np.pi)/60)
    return ((mass/1000)*2.2*32.2)*(omega**2)*(r**3)*tan((90-theta)*np.pi/180)
    
def prim_balance(t):
    i = timeIndex(t)
    d = Shifting_calcs.primary_disp[i]
    belt_force_inst = belt_force[i]
    F_s = springforce(k1, d)
    F_FW = flyweight_force(d)
    return (-belt_force_inst - F_s + F_FW)/p_move_mass

def timeIndex(t):
    for i in range(len(Shifting_calcs.table[0])):
        if t == Shifting_calcs.table[0][i]:
            return i

def primary_ramp_pos(sheave_disp):
    for i in range(len(x_ramp)):
        if sheave_disp < x_ramp[i]:
            i = i-1
            break
            
        
    return (x_ramp[i], y_ramp[i], theta[i])

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




