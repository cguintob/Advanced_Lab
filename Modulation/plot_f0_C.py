import pandas as pd
import os
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/Resonance/'
out_path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/'
C = {'Setting1':29.2,'Setting2':76.3,'Setting3':151.3,'Setting4':220.5,'Setting5':293.4,'Setting6':357.5,'Setting7':400.7}
C_err = {'Setting1':0.1,'Setting2':0.1,'Setting3':0.1,'Setting4':0.1,'Setting5':0.2,'Setting6':0.2,'Setting7':0.1}

out_df = pd.DataFrame()

def quadfit(f_peak, f0_fit, A, B):
    return -A*(f_peak-f0_fit)**2+B

for fname in os.listdir(path):
    if not ('Setting' in fname and 'csv' in fname):
        continue
    if 'Setting2' in fname:
        continue
    
    setting = fname.split('_')[0]
    df = pd.read_csv(path+fname)
    
    vmax = max(df['Vout/Vin'])
    ind = df[df['Vout/Vin']==vmax].index[0]
    
    # gets quadratic region of data
    f_peak = df.loc[ind-20:ind+20,'Frequency']
    v_peak = df.loc[ind-20:ind+20,'Vout/Vin']
    
    peak_params, peak_covar = curve_fit(quadfit, f_peak, v_peak, p0=[1,40000,1], maxfev=1000000)
    
    f0 = peak_params[0]

    out_df.loc[setting,'f0']=f0
    out_df.loc[setting,'C']=C[setting]
    out_df.loc[setting,'C_error']=C_err[setting]
    
print(out_df)

def model(C, A, L, dcp,p):
    #ceq = dcs*(C+dcp)/(C+dcs+dcp) # add external capacitance in series and in parallel
    ceq = C+dcp
    return A / (L*ceq)**p 

# Fit the data to the model function
params, covar = curve_fit(model, out_df['C'], out_df['f0'], p0=[40000,1,1,0.5], maxfev=1000000)  # Initial guess for parameter 'a'
print(params)
dC = np.arange(min(out_df['C']),max(out_df['C']),0.01)

fig, ax = plt.subplots()
sns.scatterplot(out_df,x='C',y='f0', ax=ax)
ax.plot(dC, model(dC,*params))

out_df.to_csv(out_path+'data_f0_C.csv')
