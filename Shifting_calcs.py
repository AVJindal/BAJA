#%%
from cmath import tan
from lib2to3.pygram import Symbols
from sympy import symbols, Eq, solve
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Forces import *

'''
Help: 
- patterns in acceleration are weird (see table)
- the force calculated here is F_net right? is F_net = F_belt? 
- 
'''

output_accelerations = []

#Constants
CC = 8.5                     #Centre-Centre (in)
#eta = 4.0                     #Initial Ratio

low_ratio= 4.1
high_ratio= 0.5

beta1= 12                          #Primary Sheave Angle in degrees
beta2= 13                          #Secondary Sheave Angle in degrees
mf= 420                            #flyweight mass (g) 
k1= 50                             #Primary linear spring rate(lb/in) 
k2= 21                             #Secondary linear spring rate(lb/in) 
ka2= 46                            #Secondary angular spring rate(lb*in/rad)
beltEffLength = 33.8583            #Length of belt at pitch (in)
pitchInnerOffset = 0.4             #Distance from pitch radius to inner radius of belt
pitchOuterOffset = 0.185           #Distance from pitch radius to outer radius of belt

p_move_mass= 0.7072                #mass of the primary moveable sheave (lb)
s_move_mass= 0.993135              #mass of the secondary moveable sheave (lb)
belt_mass= 0.875                   #mass of the belt (lb)

gap= 0.15                          #initial gap between the belt's sides and the sheaves before engagement.

data = pd.read_csv( 'ExportedRatioTimeValues.csv')
placeholder= np.array(data).T
table= placeholder[:, 10:1000:5]

#%%%
def radii(ratio):                       #Function that takes the ratio and returns the radii of belt on each sheave
    rho1, rho2= symbols('rho1, rho2')

    length_Eq= Eq(np.pi*(rho1+rho2)+2*((rho2-rho1)**2+CC**2)**(1/2), beltEffLength)
    eta_Eq= Eq(ratio, rho2/rho1)

    sol= solve((length_Eq,eta_Eq), (rho1,rho2))
    return sol[0]

def sec_rad(ratio):                     #returns the secondary radius at a given ratio
    return radii(ratio)[1]

def prim_rad(ratio):                    #returns the primary radius at given ratio                 
    return radii(ratio)[0]

## Design Values - part 1 
R1_low= prim_rad(low_ratio)
R2_low= sec_rad(low_ratio)

R1_high= prim_rad(high_ratio)
R2_high= sec_rad(high_ratio)

low_pshaft= R1_low - pitchInnerOffset
low_Ssheave= R2_low

high_Sinner = R2_high

def prim_displacement(radius):                          #gives primary displacement given change in radius from initial
    rad_change= radius - R1_low 
    return tan(beta1*np.pi/180)*rad_change + gap

def sec_displacement(radius):                           #gives secondary displacement given change in radius from initial
    rad_change = radius - R2_low
    return tan(beta2*np.pi/180)*rad_change + gap

def derivative(time, f):                                #secant derivative function
    prime= [(f[1]-f[0])/(time[1]-time[0])]
    for i in range(len(time)): 
        if i!=0 and i!=(len(time)-1):
            prime.append((f[i+1]-f[i-1])/(time[i+1]-time[i-1]))
        if i==(len(time)-1): 
            prime.append((f[i]-f[i-1])/(time[i]-time[i-1]))
    return np.array(prime)

prim_max_disp = (R1_high - pitchInnerOffset - low_pshaft)*tan(beta1*np.pi/180) + gap
sec_max_disp = (R2_high - pitchInnerOffset - high_Sinner)*tan(beta2*np.pi/180) + gap

## MAKE TABLE
primaryradii= np.array([prim_rad(rat) for rat in table[1]])
secondaryradii= primaryradii*table[1]
primary_disp= prim_displacement(primaryradii)/12
secondary_disp = sec_displacement(secondaryradii)/12
primary_vel= derivative(table[0], primary_disp)
secondary_vel = derivative(table[0], secondary_disp)
primary_accel= derivative(table[0], primary_vel)
secondary_accel= derivative(table[0], secondary_vel)
primary_clampF= primary_accel*p_move_mass
fig, ax = plt.subplots()
ax.plot(table[0], primary_accel)
ax.plot(table[0], primary_vel)
ax.plot(table[0], primary_disp)

plt.show()

plt.legend()
secondary_clampF= secondary_accel*s_move_mass

belt_accel= derivative(table[0], derivative(table[0], primaryradii))
belt_force= belt_accel*belt_mass

# plt.plot(table[0], primary_disp)
# plt.show()

together= np.c_[table.T, primaryradii, secondaryradii, primary_disp, secondary_disp, primary_vel, secondary_vel, primary_accel, secondary_accel, primary_clampF, secondary_clampF]
# headers= ['Time Step',"Ratio", "Primary Radius", "Secondary Radius", "Primary Displacement", "Secondary Displacement", "Primary Sheave Velocity", "Secondary Sheave Velocity", "Primary Sheave Acceleration", "Secondary Sheave Acceleration", "Primary Clamping Force", "Secondary Force"]

# finaltable= pd.DataFrame(together, columns=headers)
# finaltable.to_csv('Final Data.csv', index=False)


