# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 06:59:41 2022

@author: vzlat
"""
#Importing the neccessary modules for ploting and analysis
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import math


class Tensile_Graph: # Creating a class for the tensile graphs and each plot will be an instance of the class as required by the user's input
    def __init__(self, material): # Constructor with an attribute "material" which given by the user
        self.material = material
        
    def load_data(self):# Function that loads the correct file and creates arrays for strain and stress
        if self.material == 'aluminium':
            file = 'aluminum.csv'
        elif self.material == 'high carbon steel':
            file = 'high_carbon.csv'
        elif self.material == 'low carbon mild steel':
            file = 'mild_steel.csv'
        data = pd.read_csv(file, skiprows=[1])# The correct csv file is loaded into a pandas DataFrame
        
        strain = data["Tensile strain (Strain 1)"].to_numpy()# Numpy array for 'strain' from the csv file in (%)
        stress = data['Tensile stress'].to_numpy()#Numpy array for 'stress' from the csv file in (MPa)

        pr_strain = np.array([strain[i] for i in range(len(strain)) if strain[i] < 0.2])# Numpy array for 'proof strain' with data only from the linear region
        pr_stress = np.array(stress[0:len(pr_strain)])#Numpy array for 'proof stress' with data only from the linear region
        return strain, stress, pr_stress, pr_strain#The functions returns the previous four variables


    def linear_regress(self): #Function to calculate the Young's Modulus
        strain, stress, pr_stress, pr_strain = self.load_data() # Calling the function load_data and assigning the returned variables 
        res = stats.linregress(pr_strain,pr_stress) # Calculating the slope(Young's Modulus) of the linear region using linear regression from the 'scipy' library
        y_m = res.slope #Assigning y_m the value of the slope; 
        b = res.intercept # y-interscept value of the linear regression
        return y_m, b #The functions returns the Young's Modulus and y-intercept 
    
    def graph(self): #Function that makes the graph
        strain, stress, pr_stress, pr_strain = self.load_data() # Calling the function load_data and assigning the returned variables
        y_m,b = self.linear_regress() # Calling the function linear_regress and assigning the returned variables
        ts_stress = np.max(stress) # Tensile stress which is maximum value in array 'stress'
        fail_strain = strain[-1] # Fail strain which is the last recorded value from the array 'strain'
        proof_func = y_m*(strain-0.2) + b # The function for the y-values of 0.2% proof stress line
        idx =np.argwhere(np.diff(np.sign(stress-proof_func))).flatten()# Finding the intersection point between the stress-strain curve and the 0.2% proof stess line; this lines returnes te index of the value of the array 'strain'; NB! as discerete values are used and the the point may not be excatly where the line crosses the curve
        fig1, ax1 = plt.subplots() # Creating figure and axis
        plot = ax1.plot(strain,stress, color = 'blue', label='stress-strain curve') # Plotting the stress-strain curve
        proof_plot = ax1.plot(strain, proof_func, color = 'black') #Plotting the 0.2% proof stress line
        point = ax1.plot(strain[idx], stress[idx], "ro") # Plotting the point of intersection
        plt.ylim(0,800) #Limiting the y axis values that are displayed to creat more useful graph
        plt.xlim(0,10) #Limiting the x axis values that are displayed to creat more useful graph
        ax1.set_title("Tensile stress strain graph " + self.material)#Setting the title for each graph depending on the material
        ax1.set_xlabel("Strain(%)")#Setting x-axis label
        ax1.set_ylabel("Stress(MPa)")#Setting y-axis label
        leg = ax1.legend()#Creating legend
        plt.grid(color='r', linestyle='--')#Creating grid
        print("Young's Modulus %2f(GPa) " % (y_m/10))#Printing the Young's Modulus, divided by 10 to convert into (GPa)
        print("0.2%%proof stress : %2f(Mpa), ultimate stress: %2f(MPa), failure strain(%%): %2f" % (stress[idx], ts_stress, fail_strain) )#Priting, yield stress, tensile stress, and fail strain
        return plot # returning the plot
    
class Torsion_Graph: # Creating a class for the torsion graphs and each plot will be an instance of the class as required by the user's input
    def __init__(self, material): # Constructor with an attribute "material" which given by the user
        self.material = material
        
    def load_data(self):# Function that loads the correct file depending on the material
        r, J, L = 0,0,0# Intializing the radius, length and after that the values for each material are assigned (all in meters)
        if self.material == 'aluminium':
            file = 'tor_alum.csv'
            r, L = 0.00304,0.080
          
        elif self.material == 'cast iron':
            file = 'tor_cast.csv'
            r, L = 0.003,0.078
          
        elif self.material == 'low carbon mild steel':
            file = 'tor_steel.csv'
            r, L = 0.002975, 0.076
            
        J = (math.pi*r**4)/2#Calculating the polar moment if inertia (mm**4)
        data = pd.read_csv(file)
        
        torque = data["Torque(Nm)"].to_numpy()# Numpy array for 'torque' from the csv file in (Nm)
        angle = data["Angle"].to_numpy()# Numpy array for 'torque' from the csv file in (radians)
        
        strain = ((r/L)*angle)# Calculating strain in (-)
        stress = ((r/J)*torque)/1000000 #Calculating stress in MPa
        pr_strain = np.array(strain[0:3])# Numpy array for 'proof strain' with data only from the linear region
        pr_stress = np.array(stress[0:3])# Numpy array for 'proof stress' with data only from the linear region
        return strain, stress, pr_stress, pr_strain#The functions returns the previous four variables
#   
    def linear_regress(self):#Function to calculate the Shear Modulus
        strain, stress, pr_stress, pr_strain = self.load_data()# Calling the function load_data and assigning the returned variables 
        res = stats.linregress(pr_strain,pr_stress)# Calculating the slope(Shear Modulus) of the linear region using linear regression from the 'scipy' library
        s_m = res.slope# Assigning s_m the value of the slope(Shear Modulus); divided by 1000 to convert into GPa
        b = res.intercept# x-interscept value of the linear regression
        return s_m, b#The functions returns the Young's Modulus and x-intercept
        
    def graph(self):#Function that makes the graph
        strain, stress, pr_stress, pr_strain = self.load_data() # Calling the function load_data and assigning the returned variables
        s_m,b = self.linear_regress()# Calling the function linear_regress and assigning the returned variables
        
        fig1, ax1 = plt.subplots()# Creating figure and axis
        plot = ax1.plot(strain,stress, color = 'blue', label='stress-strain curve')# Plotting the stress-strain curve
        ax1.set_title("Shear stress strain graph " + self.material)#Setting the title for each graph depending on the material
        ax1.set_xlabel("Strain(-)")#Setting x-axis label
        ax1.set_ylabel("Shear Stress(MPa)")#Setting y-axis label
        leg = ax1.legend()#Creating legend
        plt.grid(color='r', linestyle='--')#Creating grid
        
        th = 0 # Creating th(thoughness)  
        N = len(strain)#Number of discrete intervals along x-axis
        for k in range(1, N):# 'for' loop to calculate the thoughness(area under the stress-strain curve) using the trapezium rule
            th += (stress[k-1]+stress[k]) * (strain[k]-strain[k-1])/2
        print("Shear Modulus %2f(GPa): " % (s_m/1000))#Printing the Shear Modulus in GPa
        print("thoughness %2f(MJ/m^3): " % th)#Printing the thougness in MJ/m^3
        return plot# returning the plot

class Charpey_values:
    def __init__(self, material): # Constructor with an attribute "material" which given by the user
        self.material = material
        
    def calculations(self):
        en_lost = 0.04 # Lost energy to friction and air resistance J
        if self.material == 'aluminium':
            high_t, low_t, en_h,en_l = 23,-42, (0.85-en_lost), (0.89-en_lost)
        elif self.material == 'high carbon steel':
            high_t, low_t, en_h,en_l = 23,-48, (2.87-en_lost), (0.57-en_lost)
        elif self.material == 'low carbon mild steel':
            high_t, low_t, en_h,en_l = 23,-40, (1.05-en_lost), (0.32-en_lost)
        return print("Energy absorbed at %1.2f C: %1.2f J, and %1.2f C:  %1.2f J" % (high_t, en_h, low_t, en_l))
        
def tensile_all():
    data_al = pd.read_csv('aluminum.csv', skiprows=[1])# The correct csv file is loaded into a pandas DataFrame        
    al_strain = data_al["Tensile strain (Strain 1)"].to_numpy()# Numpy array for 'strain' from the csv file in (%)
    al_stress = data_al['Tensile stress'].to_numpy()#Numpy array for 'stress' from the csv file in (MPa)
    data_hc = pd.read_csv('high_carbon.csv', skiprows=[1])# The correct csv file is loaded into a pandas DataFrame        
    hc_strain = data_hc["Tensile strain (Strain 1)"].to_numpy()# Numpy array for 'strain' from the csv file in (%)
    hc_stress = data_hc['Tensile stress'].to_numpy()#Nump   
    data_lc = pd.read_csv('mild_steel.csv', skiprows=[1])# The correct csv file is loaded into a pandas DataFrame       
    lc_strain = data_lc["Tensile strain (Strain 1)"].to_numpy()# Numpy array for 'strain' from the csv file in (%)
    lc_stress = data_lc['Tensile stress'].to_numpy()#Numpy

    fig1, ax1 = plt.subplots() # Creating figure and axis
    alum = ax1.plot(al_strain,al_stress, color = 'blue', label='Aluminium') # Plotting the stress-strain curve    
    high = ax1.plot(hc_strain,hc_stress, color = 'green', label='High Carbon Steel')
    low = ax1.plot(lc_strain,lc_stress, color = 'red', label='Low Mild Carbon Steel')
    ax1.set_title("Tensile Test")
    ax1.set_xlabel("Strain (%)")#Setting x-axis label
    ax1.set_ylabel("Stress (MPa)")#Setting y-axis label
    leg = ax1.legend(facecolor="pink")#Creating legend
    #plt.grid(color='black', linestyle='--')#Creating grid
    fig1.tight_layout
    fig1.savefig("tensile_test.png",dpi=600)
    return high



user_input = input('What test do you want?(tensile, torsion, charpey):')
if user_input == 'tensile':
    user_input = str(input("What material do you want?(aluminium, high carbon steel, low carbon mild steel or all):" ))
    if user_input == "all":
        tensile_all()
    else:
        Ten1 = Tensile_Graph(user_input)
        graph = Ten1.graph()
elif user_input == 'torsion':
    user_input = str(input("What material do you want?(aluminium, cast iron, low carbon mild steel):" ))
    Tor1 = Torsion_Graph(user_input)
    graph = Tor1.graph()
elif user_input == 'charpey':
    user_input = str(input("What material do you want?(aluminium, high carbon steel or low carbon mild steel):" ))
    Ch1 = Charpey_values(user_input)
    val = Ch1.calculations()


    