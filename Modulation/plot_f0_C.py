import pandas as pd
import os
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Exp 2/Resonance/'

C = {'Setting1':29.2,'Setting2':76.3,'Setting3':151.3,'Setting4':220.5,'Setting5':293.4,'Setting6':357.5,'Setting7':400.7}
C_err = {'Setting1':0.1,'Setting2':0.1,'Setting3':0.1,'Setting4':0.1,'Setting5':0.2,'Setting6':0.2,'Setting7':0.1}

out_df = pd.DataFrame()

for fname in os.listdir(path):
    if not 'csv' in fname:
        continue
    setting = fname.split('_')[0]
    df = pd.read_csv(path+fname)
    vout_vin_max = max(df['Vout/Vin'])
    ind = df[df['Vout/Vin']==vout_vin_max].index
    f0 = int(df['Frequency'].iloc[ind])
    
    out_df.loc[setting,'f0']=f0
    out_df.loc[setting,'C']=C[setting]
    out_df.loc[setting,'C_error']=C_err[setting]
    
print(out_df)

def model(C, A, L, p):
    return A / (L*C)**p 

# Fit the data to the model function
params, covar = curve_fit(model, out_df['C'], out_df['f0'], p0=[40000,1,0.5], maxfev=1000000)  # Initial guess for parameter 'a'
print(params)
dC = np.arange(min(out_df['C']),max(out_df['C']),0.01)

fig, ax = plt.subplots()
sns.scatterplot(out_df,x='C',y='f0', ax=ax)
ax.plot(dC, model(dC,*params))
