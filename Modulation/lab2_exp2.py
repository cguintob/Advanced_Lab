import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import re

points = 40
colors = ["cyan", "green", "black", "magenta", "blue", "orange", "purple", "yellow", "dimgray"]
nticks = 4
fontsize = 8
labelsize = 5
sp_row = 2
sp_col = 3
percent = 0.942
npercs = 100

def series_ticks(series, n):
    return (max(series.astype(float)) - min(series.astype(float))) / n

def list_ticks(ls, n):
    return (max(ls) - min(ls)) / n

def closest(ls, K):
     ls = np.asarray(ls)
     idx = (np.abs(ls - K)).argmin()
     return ls[idx]

def plotter_raw(axis, i, j, x, y):
    axis[i, j].plot(x, y, colors[(sp_col * i) + j])
    axis[i, j].set_xlabel("Vin", fontsize = fontsize)
    axis[i, j].set_ylabel("Derivative", fontsize = fontsize)
    axis[i, j].set_xlim(min(x), max(x))
    axis[i, j].set_ylim(min(y), max(y))
    axis[i, j].set_xticks(np.arange(min(x.astype(float)), max(x.astype(float)) + 1, series_ticks(x, nticks)))
    axis[i, j].set_yticks(np.arange(min(y.astype(float)), max(y.astype(float)) + 1, series_ticks(y, nticks)))
    axis[i, j].tick_params(labelsize = labelsize)
    axis[i, j].set_title(labels[(sp_col * i) + j], fontsize = fontsize)
    axis[i, j].set_title(labels[(sp_col * i) + j], fontsize = fontsize)

def plotter_deriv(axis, i, j, x, y):
    axis[i, j].plot(x, y, colors[(sp_col * i) + j])
    axis[i, j].set_xlabel("Vin", fontsize = fontsize)
    axis[i, j].set_ylabel("Derivative", fontsize = fontsize)
    axis[i, j].set_xlim(min(x), max(x))
    axis[i, j].set_ylim(min(y), max(y))
    axis[i, j].set_xticks(np.arange(min(x.astype(float)), max(x.astype(float)) + 1, series_ticks(x, nticks)))
    axis[i, j].set_yticks(np.arange(min(y), max(y) + 1, list_ticks(y, nticks)))
    axis[i, j].tick_params(labelsize = labelsize)
    axis[i, j].set_title(labels[(sp_col * i) + j], fontsize = fontsize)
    axis[i, j].set_title(labels[(sp_col * i) + j], fontsize = fontsize)

files = []
labels = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):
        if (sys.argv[i].endswith(".csv")):
            name = re.split(r"[/.]+", sys.argv[i])
            name_split = name[1].split("_")
            if ("Diode2" not in name_split and "Resistor" not in name_split):
                files.append(sys.argv[i])
                labels.append(name[1])
            else:
                continue
        else:
            print("Incorrect format.")
            sys.exit(1)

figure1, axis1 = plt.subplots(sp_row, sp_col)

for i in range(sp_row):
    for j in range(sp_col):
        df = pd.read_csv(files[(sp_col * i) + j], sep = ",", engine = "python")
        plotter_raw(axis1, i, j, df["Vin"], df["Vout"])

figure1.suptitle("Output vs. Input Voltages for Diodes and Resistor")
plt.tight_layout()

figure2, axis2 = plt.subplots(sp_row, sp_col)
derivatives = []

for i in range(sp_row):
    for j in range(sp_col):
        df = pd.read_csv(files[(sp_col * i) + j], sep = ",", engine = "python")
        for k in range(len(df["Vout"]) - 1):
            derivatives.append((df.at[k + 1, "Vout"] - df.at[k, "Vout"]) / (df.at[k + 1, "Vin"] - df.at[k, "Vin"]))
        plotter_deriv(axis2, i, j, df["Vin"][:-1], derivatives)
        derivatives.clear()

figure2.suptitle("Numerical Differentiation")
plt.tight_layout()

figure3, axis3 = plt.subplots(sp_row, sp_col)
avg_const = 0
threshs = []
percents = []

for i in range(sp_row):
    for j in range(sp_col):
        df = pd.read_csv(files[(sp_col * i) + j], sep = ",", engine = "python")
        for k in range(len(df["Vout"]) - 1):
            derivatives.append((df.at[k + 1, "Vout"] - df.at[k, "Vout"]) / (df.at[k + 1, "Vin"] - df.at[k, "Vin"]))
        for k in range(1, len(derivatives)):
            if (np.abs(derivatives[k] - derivatives[k - 1]) > 0.1):
                derivatives[k] = derivatives[k - 1]
        plotter_deriv(axis3, i, j, df["Vin"][:-1], derivatives)
        if (derivatives.index(max(derivatives)) - 10 < 0):
            avg_const = sum(derivatives[0:points]) / points
        else:
            avg_const = sum(derivatives[len(derivatives) - (points + 1):len(derivatives) - 1]) / points
        thresh_vout = percent * avg_const
        close = closest(derivatives, thresh_vout)
        index = derivatives.index(close)
        thresh_vin = df["Vin"][:-1][index]
        print("Threshold Voltage of " + labels[(sp_col * i) + j] + ": " + str(round(thresh_vin, 4)))
        axis3[i, j].axvline(x = thresh_vin)
        axis3[i, j].axhline(y = percent * avg_const)
        derivatives.clear()

figure3.suptitle("Numerical Differentiation: Data Cleaned")
plt.tight_layout()

plt.show()
            







'''



for k in range(npercs):
thresh_in = df["Vin"][:-1][derivatives.index(closest(derivatives, (k / npercs) * avg_const))]
new_thresh_in = df["Vin"][:-1][derivatives.index(closest(derivatives, ((k + 1) / npercs) * avg_const))]
if (np.abs(new_thresh_in) - thresh_volt < np.abs(thresh_in) - thresh_volt):
min_thresh = np.abs(new_thresh_in)
min_percent = (k + 1) / npercs
elif (np.abs(new_thresh_in) - thresh_volt >= np.abs(thresh_in) - thresh_volt):
min_thresh = np.abs(thresh_in)
min_percent = k / npercs
print(thresh_in, new_thresh_in, min_thresh)
threshs.append(min_thresh)
percents.append(min_percent)

'''
















'''
for k in range(npercs + 1):
percent = k / npercs
percents.append(percent)
thresh_vout = percent * max(derivatives)
close = closest(derivatives, thresh_vout)
index = derivatives.index(close)
thresh_vin.append(df["Vin"][:-1][index])
true_thresh_vin.append(min(thresh_vin))
'''




'''
for k in range(1, npercs):
if (closest_error_upper[k] - 0.6 > closest_error_upper[k - 1] - 0.6):
true_thresh_upper = closest_error_upper[k - 1]
else:
true_thresh_upper = closest_error_upper[k + 1]
if (closest_error_lower[k] + 0.6 < closest_error_lower[k - 1] + 0.6):
true_thresh_lower = closest_error
'''



'''
if ("Diode4" in labels[(sp_col * i) + j].split("_")):
thresh_volt = 0.25
else:
thresh_volt = 0.65
if (derivatives[len(derivatives) - 1] - derivatives[0] < 0):
thresh_volt *= -1
else:
thresh_volt *= 1
thresh_vin = closest(df["Vin"][:-1], thresh_volt)
index = list(df["Vin"][:-1]).index(thresh_vin)
thresh_vout = derivatives[index]
'''


'''
if (derivatives.index(max(derivatives)) - 10 < 0):
avg_const = sum(derivatives[0:points]) / points
for k in range(points):
sum_squared += (derivatives[k] - avg_const) * (derivatives[k] - avg_const)
else:
avg_const = sum(derivatives[len(derivatives) - (points + 1):len(derivatives) - 1]) / points
for k in range(points):
sum_squared += (derivatives[len(derivatives) - (k + 1)] - avg_const) * (derivatives[len(derivatives) - (k + 1)] - avg_const)
variance = sum_squared / (points - 1)
stdev = np.sqrt(variance)
sterr = stdev / np.sqrt(points)
print(str(avg_const) + " +/- " + str(stdev))
sum_squared = 0
'''
