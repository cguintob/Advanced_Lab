import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from scipy.optimize import curve_fit

def function(x, a, b, c):
    y = a/(x + b)**c
    return y

files = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):
        if (sys.argv[i].endswith(".txt")):
            if (i == 1):
                background = sys.argv[i]
            else:
                files.append(sys.argv[i])
        else:
            print("Incorrect format.")
            sys.exit(1)
else:
    print("Incorrect format.")
    sys.exit(1)

files = sorted(files, key = lambda x: float(x[:-len(".txt")]))
live_times = [43574, 240.46, 240.54, 240.64, 240.49, 240.55, 240.53, 240.58, 240.71, 240.63, 243.52, 240.74, 240.51, 314.92, 240.5, 240.56, 180, 180, 180, 181, 180]
distances = [0.0, 1.4, 2.4, 3.4, 4.5, 5.5, 6.6, 7.5, 8.3, 9.3, 10.3, 11.5, 12.5, 13.5, 14.5, 15.65, 16.2, 16.7, 17.2, 17.9]
integrals = []
summation = 0
lower_channel = 1060
upper_channel = 1390
indexer = 1

for f in files:
    try:
        df_back = pd.read_csv(background, sep = "\r\n", header = None, engine = "python")
        df_back[0] = df_back[0].apply(lambda x: x.replace("\t", " "))
        df_back[["Channel", "Energy", "Count"]] = df_back[0].str.split(" ", n = 2, expand = True)
        df_back.drop([0], axis = 1, inplace = True)
        df_back.set_index("Channel", inplace = True)
        df = pd.read_csv(f, sep = "\r\n", header = None, engine = "python")
        df[0] = df[0].apply(lambda x: x.replace("\t", " "))
        df[["Channel", "Energy", "Count"]] = df[0].str.split(" ", n = 2, expand = True)
        df.drop([0], axis = 1, inplace = True)
        df.set_index("Channel", inplace = True)
        df_back["Count"] = df_back["Count"].astype("float") * (float(live_times[indexer]) / float(live_times[0]))
        for i in range(len(df.index)):
            if ((float(df.iloc[i, 1]) - float(df_back.iloc[i, 1])) < 0):
                df.iloc[i, 1] = 0
            else:
                df.iloc[i, 1] = float(df.iloc[i, 1]) - float(df_back.iloc[i, 1])
        for i in range(lower_channel, upper_channel + 1):
            summation += float(df.iloc[i, 1])
        integrals.append(float(summation) / float(live_times[indexer]))
        indexer += 1
        summation = 0
    except FileNotFoundError:
        print("Couldn't find file.")
        sys.exit(1)

for i in range(len(distances)):
    print(str(distances[i]) + " " + str(integrals[i]))

parameters, covariance = curve_fit(function, distances, integrals, p0 = [40000, 3, 2])
print(parameters)
fit_x = np.arange(min(distances), max(distances), 0.01)
fit_y = function(fit_x, *parameters)
plt.scatter(distances, integrals, color = "b", label = "Data")
plt.plot(fit_x, fit_y, color = "y", label = "Fit")
plt.xlabel("Distance [cm]")
plt.ylabel("Integrated Count")
plt.title("Integrated Count vs. Distance for Cs-137 Gamma Spectrum")
plt.legend()
plt.show()

'''
residuals = integrals - fit_y
ss_res = np.sum(residuals**2)
ss_tot = np.sum((integrals - np.mean(integrals))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)
'''
