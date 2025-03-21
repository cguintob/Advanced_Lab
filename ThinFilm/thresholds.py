import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from scipy.optimize import curve_fit

def function(x, a, b, c):
    y = a * (x + b)**c
    return y

files = []
try:
    for i in range(1, len(sys.argv)):
        files.append(sys.argv[i])
except FileNotFoundError:
    print("Data file not found.")
    sys.exit(1)

for f in files:
    df = pd.read_csv(f, sep = ",", engine = "python")
    df.dropna(axis = 1, inplace = True)
    df.rename(columns = {"d [kA]": "Thickness", "d with offset": "Offset", "V_s (mV)": "V_s", "V_bias (mV)": "V_bias", "Current [A] V_bias/10kOhm": "Current", "Resistance [Ohms] V_s/Current": "Resistance", "Resistivity [S/m] R*(d*width)/length": "Resistivity", "Conductivity [1/Resistivity]": "Conductivity"}, inplace = True)
    df["Offset"] = df["Offset"].apply(lambda x: 100 * x)
    for i in range(len(df["Conductivity"])):
        if (df["Conductivity"][i] < 0):
            df.drop(i, inplace = True)
    df.reset_index(drop = True, inplace = True)
    for i in range(len(df["Conductivity"])):
        if (i < df["Conductivity"].idxmin()):
            df.drop(i, inplace = True)
    df.reset_index(drop = True, inplace = True)
    for i in range(1, len(df["Conductivity"])):
        if (np.abs(df["Conductivity"][i] - df["Conductivity"][i - 1]) > 100000):
            for j in range(i, len(df["Conductivity"])):
                df.drop(j, inplace = True)
            break
    df.reset_index(drop = True, inplace = True)
    for i in range(1, len(df["Conductivity"]) - 1):
        if (np.abs(df["Conductivity"][i] - df["Conductivity"][i - 1]) > 45000):
            df.drop(i - 1, inplace = True)
    df.reset_index(drop = True, inplace = True)
    
    parameters, covariance = curve_fit(function, df["Offset"], df["Conductivity"], p0 = [200000, -0.05, 0.25])
    fit_x = np.arange(min(df["Offset"]), max(df["Conductivity"]), 0.01)
    fit_y = function(fit_x, *parameters)
    
    plt.scatter(df["Offset"], df["Conductivity"], color = "b", label = "Data")
    plt.plot(fit_x, fit_y, color = "y", label = "Fit")
    plt.title("Conductivity vs. Thickness")
    plt.xlabel("Thickness [nm]")
    plt.ylabel("Conductivity [1/\u03A9]")
    plt.xlim([0, 75])
    plt.ylim([0, 250000])
    plt.legend()

    zero = str(round(-parameters[1], 5))
    print("Expected thickness for conductivity: " + zero + " nm")
    
plt.show()
