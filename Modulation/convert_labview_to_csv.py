import pandas as pd
import os

path = 'C:/Users/cjhuc/OneDrive/SY 2024-2025/Advanced Lab/Exp 2/Resonance/'

cols = ['Frequency', 'Vout/Vin', 'Vin', 'Vout']

for fname in os.listdir(path):
    if 'csv' in fname:
        continue
    f = open(path+fname, 'r')
    f.readline()
    
    rows = []
    for i,line in enumerate(f):
        line = line.split('	')
        row = []
        for num in line:
            try:
                num = float(num)
                row.append(num)
            except:
                pass
        row = pd.DataFrame(row).T
        rows.append(row)
    f.close()    
    
    df = pd.concat(rows, axis = 0)
    df.columns = cols
    df = df.reset_index(drop=True)
    print(df)

    df.to_csv(path+fname+'.csv', index=False)
    