import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from scipy.optimize import curve_fit

files = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):
        files.append(sys.argv[i])
else:
    print("Incorrect format.")
    sys.exit(1)

frequencies = []
maxima = []
for f in files:
    try:
        df = pd.read_csv(f, sep = ",", header = None, engine = "python")
        df.columns = ["Frequency", "V_out/V_in", "V_in", "V_out"]
        frequencies.append(df.loc[df["V_out/V_in"].idxmax()])
        maxima.append(max(df["V_out/V_in"]))
    except FileNotFoundError:
        print("File " + f + "not found.")
        sys.exit(1)

for i in range(len(frequencies)):
    print(frequencies[i])

for i in range(len(maxima)):
    print(maxima[i])

    
        
