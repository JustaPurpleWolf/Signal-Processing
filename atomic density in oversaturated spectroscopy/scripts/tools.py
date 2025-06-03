import os 
import numpy as np 
import pandas as pd
import json
import scipy.constants as cte
import matplotlib.pyplot as plt 
import matplotlib.image as mpimgs
from pathlib import Path
from scipy.optimize import curve_fit
from scipy import special

def create_directory(directory):
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def quad(x, a, b, c): # ajuste cuadrático para borrar ruido de fondo y normalizar la señal
    return a*x**2 + b*x + c 

def adjust_frec_peaks(time, peaks):
    with open('constants.json', 'r') as openfile:
        vals = json.load(openfile) # Reading from json file
    exp, teo = [], []
    for i in range(0,4):
        for peak in peaks[i]: exp.append(peak)
        for peak in vals['frec_peaks'][i]: teo.append(peak)
    popt, pcov =  curve_fit(quad,time[exp], teo)
    frec = quad(time, *popt)*1e9
    
    fig = plt.figure(figsize=(6,4))
    plt.plot(time[exp], np.array(teo)*1e9, label = "peaks", linewidth = 1.5)
    plt.plot(time, frec, '--', label = "fit", linewidth = 1.5)
    plt.xlabel('time [s]'), plt.ylabel('frec [Hz]'), plt.grid()
    plt.title(f'Frequency fit')
    plt.legend()
    plt.show()
    return frec

def adjust_noise(data, time, bound, noise):
    x_bkg =  pd.concat([time[bound[0]:bound[1]], time[bound[2]:bound[3]], time[bound[4]:bound[5]],time[bound[6]:bound[7]]])
    y_bkg = pd.concat([data[bound[0]:bound[1]], data[bound[2]:bound[3]], data[bound[4]:bound[5]],data[bound[6]:bound[7]]])

    popt, pcov = curve_fit(quad, x_bkg, y_bkg) # se realiza el ajuste 
    eval = quad(time, *popt)
    noiseless = data/eval # quitars ruido de fondo
    return (noiseless-noise)/(noiseless.max()-noise) # normalización

def density(constant, T, V):
    p = 10**(constant[0] + constant[1]/T  +  constant[2]*T + constant[3]*np.log10(T))
    N = (p*V)/(cte.k*T)
    return N

def voigt(x, x0, params=[0,0,0,0]): # params = (k,u, gamma, detuning)
    y = 2*np.pi*(x-params[3]*1e6+x0)/(params[0]*params[1])
    a = params[2]/(params[0]*params[1])
    erfc_term = special.erfc(a/2-1j*y)+np.exp(1j*2*a*y)*special.erfc(a/2+1j*y)
    return np.abs(np.sqrt(np.pi)/(2*params[0]*params[1])*np.exp(1/4*(a-1j*2*y)**2)*erfc_term)

def absorption_p(x, x0, T, N):
    with open('constants.json', 'r') as openfile:
        vals = json.load(openfile) # Reading from json file
    
    u_85 = np.sqrt((2*cte.k*T)/vals['M_85'])
    u_87 = np.sqrt((2*cte.k*T)/vals['M_87'])
   
    const_85 = (vals['k']*N*vals['Q_85']*vals['d_D2']**2)/(vals['g_I85']*cte.epsilon_0*cte.hbar)
    const_87 = (vals['k']*N*vals['Q_87']*vals['d_D2']**2)/(vals['g_I87']*cte.epsilon_0*cte.hbar)
    
    coeff = 0
    for i in [0,1,2,5,6,7]:
        coeff += const_85*voigt(x, x0, params = [u_85, vals['k'], vals['GammaD2'], vals['det_85'][i]])*vals['Cge_85'][i] #C_F^2 = Cge[i]
        coeff += const_87*voigt(x, x0, params = [u_87, vals['k'], vals['GammaD2'], vals['det_87'][i]])*vals['Cge_87'][i]
    return np.exp(-vals['L']*coeff)