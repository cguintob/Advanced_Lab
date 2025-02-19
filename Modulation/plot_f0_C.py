import pandas as pd
import os
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/Resonance2/'
out_path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/'
# C = {'Setting1':29.2,'Setting2':76.3,'Setting3':151.3,'Setting4':220.5,'Setting5':293.4,'Setting6':357.5,'Setting7':400.7}
# C_err = {'Setting1':0.1,'Setting2':0.1,'Setting3':0.1,'Setting4':0.1,'Setting5':0.2,'Setting6':0.2,'Setting7':0.1}

C = {'Setting1':403.3,'Setting2':380.1,'Setting2-5':376.1,'Setting3':321.3,'Setting4':241.4,'Setting5':180.35,'Setting6':111.35,'Setting6-5':59.40,'Setting7':34.25}
C_err = {'Setting1':0.1,'Setting2':0.1,'Setting2-5':0.2, 'Setting3':0.1,'Setting4':0.1,'Setting5':0.1,'Setting6':0.1,'Setting6-5':0.1,'Setting7':0.1}

out_df = pd.DataFrame()

def quadfit(f_peak, f0_fit, A, B):
    return -A*(f_peak-f0_fit)**2+B

i=0
for fname in os.listdir(path):
    if not ('Setting' in fname and 'csv' in fname):
        continue
    setting = fname.split('_')[0]
    # if any([setting=='Setting7']): # choose data points to exclude for testing
    #     continue
    
    df = pd.read_csv(path+fname)
    
    vmax = max(df['Vout/Vin'])
    ind = df[df['Vout/Vin']==vmax].index[0]
    
    # gets quadratic region of data
    f_peak = df.loc[ind-20:ind+20,'Frequency']
    v_peak = df.loc[ind-20:ind+20,'Vout/Vin']
    
    peak_params, peak_covar = curve_fit(quadfit, f_peak, v_peak, p0=[1,40000,1], maxfev=1000000)
    
    #print(peak_params)
    
    f0 = peak_params[0]
    
    out_df.loc[i,'Setting']=fname
    out_df.loc[i,'f0']=f0
    out_df.loc[i,'C']=C[setting]
    out_df.loc[i,'C_error']=C_err[setting]
    i+= 1
print(out_df)

def model(C, A, L,dc,p):
    #p=0.5
    #ceq = dc*C/(C+dc) # series
    ceq = C+dc # parallel
    return A / (L*ceq)**p 

# Fit the data to the model function
params, covar = curve_fit(model, out_df['C'], out_df['f0'], p0=[40000,1,10,0.5], maxfev=1000000)  # Initial guess for parameter 'a'
print(params)
sigma = np.sqrt(np.diag(covar))
print('Error',sigma)
dC = np.arange(min(out_df['C']),max(out_df['C']),0.01)

fig, ax = plt.subplots()
sns.scatterplot(out_df,x='C',y='f0',ax=ax)
ax.plot(dC, model(dC,*params))
ax.set_ylabel('Resonant Frequency, kHz')
ax.set_xlabel('Capacitance, pF')
ax.set_title('Tank Circuit Resonance')

plt.savefig(out_path+'LC_resonance_curve.jpg',dpi=600,bbox_inches='tight')
out_df.to_csv(out_path+'data_f0_C.csv')
