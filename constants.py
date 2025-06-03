import os 
import numpy as np 
import pandas as pd
import json
from pathlib import Path
import scipy.constants as cte
frec_peaks = []  # in GHz
frec_peaks.append([-2.561005-0.229851, -2.561005-0.072911, -2.561005+0.266650])
frec_peaks.append([-2.561005+1.296117-0.083835, -2.561005+1.296117-0.020435, -2.561005+1.296117+0.120640])
frec_peaks.append([4.271676-2.500832])
frec_peaks.append([4.271676])

dictionary = {
    "lambda": 780.241209e-9,    # Longitud de onda para la línea D2 en metros

    "frec_D2" : 384230426.6,    # frecuencia para línea D2 en MHz
    "frec_D1" : 377107407.299,  # frecuencia para línea D1 en MHz

    "w32" : 384.230406373*2*np.pi*1e12,
    "w12" : 377.107385690*2*np.pi*1e12,
    "wd" : (cte.c/(810e-9))*2*np.pi,
    "d13" : 384.230406373*2*np.pi*1e12 - (cte.c/(810e-9))*2*np.pi,  # w32-wd
    "d12" : 377.107385690*2*np.pi*1e12 - (cte.c/(810e-9))*2*np.pi, # w12-wd

    "M_85" : 1.40999344065e-25,    # masa en kg  84.911794u en unidades de masa atómica 
    "M_87" : 1.44316060e-25,    #  masa en kg

    "d_D2" : 5.177*cte.physical_constants['Bohr radius'][0]*cte.e,
    "d_D1" : 5.182*cte.physical_constants['Bohr radius'][0]*cte.e,

    "I87" : 3/2,
    "I85" : 5/2,
    "g_I87" : (2*(3+1)), #(2*(2*I87+1))
    "g_I85" : (2*(5+1)), # (2*(2*I85+1))
    "Q_87" : 0.2783,
    "Q_85" : 0.7217,
    "k" : 2*np.pi/780.241209e-9, # 2 pi / lambda

    "GammaD1" : 2*np.pi*5.7500e6,
    "GammaD2" : 2*np.pi*6.0666e6,

    "Rb_solid" : [4.857, -4215, 0, 0],
    "Rb_liquid" : [8.316, -4275,0, -1.3102],

    "Rb_solid_NES" : [-91.92326, -1961.258, -0.03771687, 42.57526],
    "Rb_liquid_NES" : [18.00753, -4529.635, 0.00058663, -2.991382],

    "Rb_solid_ALC" : [-9.863, -4215, 0, 0],
    "Rb_liquid_ALC" : [9.318, -4040, 0, 0],
    
    "L" : 0.10, # Calor Latente de Vaporización o Sublimación del Rubidio

    # Transition strength of RB 85 of D2 line (C_F^2)
    #Fg2_1 = 1/3, Fg2_2 = 35/81, Fg2_3 = 28/81, Fg2_4 = 0, Fg3_1 = 0, Fg3_2 = 10/81, Fg3_3 = 35/81, Fg3_4 = 1
    "Cge_85" : [1/3, 35/81, 28/81, 0,0,10/81, 35/81,1],

    # Transition strength of RB 87
    #Fg1_0 = 1/9, Fg1_1 = 5/18, Fg1_2 = 5/18, Fg1_3 = 0, Fg2_0 = 0, Fg2_1 = 1/18, Fg2_2 = 5/18, Fg2_3 = 7/9
    "Cge_87" : [1/9, 5/18, 5/18, 0,0,1/18, 5/18,7/9],

    # detunings 85Rb D2 line
    #d2_1 = 1635.454, d2_2= 1664.714, d2_3= 1635.454, d2_4 = 0, d3_1 = 0d3_2 =-1371.29, d3_3=-1307.87, d3_4=-1186.91
    "det_85" : [1635.454,1664.714,1728.134,0, 0, -1371.29,-1307.87,-1186.91],

    # detunings 87Rb D2 line
    #d1_0= 4027.403, d1_1= 4099.625,d1_2 = 4256.57,d1_3= 0 , d2_0 = 0 ,d2_1 =-2735.05, d2_2=-2578.11, d2_3=-2311.26
    "det_87" : [4027.403,4099.625,4256.57,0,0, -2735.05,-2578.11,-2311.26],

    "frec_peaks" : [[-2.561005+0.266650-0.193741, -2.561005+0.266650-0.1333, -2.561005+0.266650],[-2.561005+1.296117-0.083835, -2.561005+1.296117-0.020435, -2.561005+1.296117+0.120640],[4.271676-2.500832], [4.271676-0.07847]] #[-2.561005-0.229851, -2.561005-0.072911, -2.561005+0.266650] in GHz

}

with open("constants.json", "w") as outfile:
    json.dump(dictionary, outfile)