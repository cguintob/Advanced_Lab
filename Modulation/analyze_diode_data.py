import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# USED THIS SECTION TO MAKE DIFFERENTIATED DATA FILES
# (LATER CLEANED MANUALLY USING CAPSTONE)

#path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/diodedata/'

# for f in os.listdir(path):
#     if not 'csv' in f:
#         continue
#     if 'Resistor' in f:
#         continue
    
#     fname = f.split('.csv')[0]
    
#     df = pd.read_csv(path+f)
#     #print(df)
#     # fig,ax = plt.subplots()
#     # sns.lineplot(data=df,x='Vin',y='Vout', ax=ax)
#     #ax.set_title(f)
    
#     h = 0.1
#     vout_diff = np.diff(df['Vout'])/h
#     vin = [(df.loc[i,'Vin']+df.loc[i+1,'Vin'])/2 for i in df.index if i<df.index[-1]]
    
#     out_df = pd.DataFrame()
#     out_df['Vin'] = vin
#     out_df['Vout'] = vout_diff
    
#     out_df.to_csv(path+fname+'_diff.csv', index=False)
    
#     fig2,ax2 = plt.subplots()
#     ax2.plot(vin,vout_diff)
#     ax2.set_title(f+' Differentiated')

ref = pd.read_csv('C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/diode_diff_final_constant.csv', index_col=0)
df = pd.read_csv('C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Signal Modulation/diodedata/cleaned_diode_data.csv')

tests = ['D1-1','D1-2','D3-1','D3-2','D4-1','D4-2']

ge = 0.6
si = 0.3

threshold = 0.9
print('Trying thresholds')
while threshold < 1:
    within_uncertainty = {t:0 for t in tests}
    large_err_flag = 0
    for t in tests:
        Vin = t+'-in'
        Vout = t+'-out'
        
        diode = t.split('-')[0][-1]
        diode = int(diode)
        direction = t.split('-')[1]
        direction = int(direction)
        
        avg = ref.loc[diode,'dir'+str(direction)+' mean']
        stdev = ref.loc[diode,'dir'+str(direction)+' stdev']
        count = ref.loc[diode,'dir'+str(direction)+' count']
        
        err = stdev/np.sqrt(count)
        
        temp = np.nan
        vind = np.nan
        diff = np.nan
        
        for di in df.index:
            diff_temp = np.abs(df.loc[di,Vout]-threshold*avg)
            if np.isnan(diff):
                diff = diff_temp
                vind = di
            elif diff_temp < diff:
                diff = diff_temp
                vind = di
        vin = df.loc[vind,Vin]
        
        dy = np.diff(df[Vout])[vind]
        vin_err = abs(err/dy)
        
        if abs(vin_err) > 1:
            large_err_flag = 1
        
        if (abs(vin) + vin_err >= ge and abs(vin) - vin_err <= ge):
            within_uncertainty[t]='ge'
        elif (abs(vin)+vin_err >= si and abs(vin) - vin_err <= si):
            within_uncertainty[t]='si'
       
    bad_count = sum(1 for value in within_uncertainty.values() if value == 0)
    
    if (0 not in within_uncertainty.values() and large_err_flag ==0):
        print('Selected threshold:',threshold)
        break
    
    threshold += 0.001


for t in tests:
    Vin = t+'-in'
    Vout = t+'-out'
    
    diode = t.split('-')[0][-1]
    diode = int(diode)
    direction = t.split('-')[1]
    direction = int(direction)
    
    avg = ref.loc[diode,'dir'+str(direction)+' mean']
    stdev = ref.loc[diode,'dir'+str(direction)+' stdev']
    count = ref.loc[diode,'dir'+str(direction)+' count']
    
    err = stdev/np.sqrt(count)
    
    temp = np.nan
    vind = np.nan
    diff = np.nan
    
    for di in df.index:
        diff_temp = np.abs(df.loc[di,Vout]-threshold*avg)
        if np.isnan(diff):
            diff = diff_temp
            vind = di
        elif diff_temp < diff:
            diff = diff_temp
            vind = di
    vin = df.loc[vind,Vin]
    
    dy = np.diff(df[Vout])[vind]
    vin_err = abs(err/dy)
    
    print('Diode',diode,'Direction',direction)
    print('V_in = ',vin,'+/-',round(vin_err,7))
    
    if (abs(vin) + vin_err >= ge and abs(vin) - vin_err <= ge):
        within_uncertainty[t]='ge'
        print('Within uncertainty of Ge = 0.6')

    elif (abs(vin)+vin_err >= si and abs(vin) - vin_err <= si):
        within_uncertainty[t]='si'
        print('Within uncertainty of Si = 0.3')
        