#%%
from cmath import tan
from lib2to3.pygram import Symbols
from sympy import symbols, Eq, solve
import numpy as np
import pandas as pd

CC = 8.5                     #Centre-Centre (in)
# eta = 4.0                     #Initial Ratio

low_ratio= 4.1
high_ratio= 0.5

beta1= 12                     #Primary Sheave Angle in degrees
beta2= 13                     #Secondary Sheave Angle in degrees
mf= 420                       #flyweight mass (g) 
k1= 50                       #Primary linear spring rate(lb/in) 
k2= 21                       #Secondary linear spring rate(lb/in) 
ka2= 46                      #Secondary angular spring rate(lb*in/rad)
beltEffLength = 33.8583     #Length of belt at pitch (in)
pitchInnerOffset = 0.4      #Distance from pitch radius to inner radius of belt
pitchOuterOffset = 0.185   # Distance from pitch radius to outer radius of belt

gap= 0.15                   #initial gap between the belt's sides and the sheaves before engagement.

data = pd.read_csv( 'ExportedRatioTimeValues.csv')
placeholder= np.array(data).T
table= placeholder[:, 0:400]


#%%%
def radii(ratio): 
    rho1, rho2= symbols('rho1, rho2')

    length_Eq= Eq(np.pi*(rho1+rho2)+2*((rho2-rho1)**2+CC**2)**(1/2), beltEffLength)
    eta_Eq= Eq(ratio, rho2/rho1)

    sol= solve((length_Eq,eta_Eq), (rho1,rho2))
    return sol[0]

def sec_rad(ratio):
    return radii(ratio)[1]

def prim_rad(ratio): 
    return radii(ratio)[0]

## Design Values - part 1 
R1_low= prim_rad(low_ratio)
R2_low= sec_rad(low_ratio)

R1_high= prim_rad(high_ratio)
R2_high= sec_rad(high_ratio)

low_pshaft= R1_low - pitchInnerOffset
low_Ssheave= R2_low

high_Sinner = R2_high

def prim_displacement(radius):
    rad_change= radius -pitchInnerOffset - low_pshaft
    return tan(beta1*np.pi/180)*rad_change + gap 

def sec_displacement(radius):
    rad_change= radius -pitchInnerOffset - high_Sinner
    return tan(beta2*np.pi/180)*rad_change + gap 

def acceleration(time, disp):
    accel= [0]
    for i in range(len(time)): 
        if i!=0:
            accel.append((disp[i]-disp[i-1])/(time[i]-time[i-1]))
    return np.array(accel)


prim_max_disp = prim_displacement(R1_high)
sec_max_disp = sec_displacement(R2_high)

## MAKE TABLE
primaryradii= np.array([prim_rad(rat) for rat in table[1]])
secondaryradii= primaryradii*table[1]
primary_disp= prim_displacement(primaryradii)
secondary_disp = sec_displacement(secondaryradii)
primary_accel= acceleration(table[0], primary_disp)
secondary_accel = acceleration(table[0], secondary_disp)

together= np.c_[table.T, primaryradii, secondaryradii, primary_disp, secondary_disp, primary_accel, secondary_accel]
headers= ['Time Step',"Ratio", "Primary Radius", "Secondary Radius", "Primary Displacement", "Secondary Displacement", "Primary Sheave Acceleration", "Secondary Sheave Acceleration"]

finaltable= pd.DataFrame(together, columns=headers)
finaltable.to_csv('Final Data.csv', index=False)
