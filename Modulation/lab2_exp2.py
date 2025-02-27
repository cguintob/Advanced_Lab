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
npercs = 1000

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
    axis[i, j].set_ylabel("Vout", fontsize = fontsize)
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
plt.savefig("Out_vs_In.png")


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
plt.savefig("Diff_vs_In.png")

avg_const = 0
diff = []
avgs = []
perc = []

for k in range(npercs + 1):
    percent = k / npercs
    for i in range(sp_row):
        for j in range(sp_col):
            df = pd.read_csv(files[(sp_col * i) + j], sep = ",", engine = "python")
            for l in range(len(df["Vout"]) - 1):
                derivatives.append((df.at[l + 1, "Vout"] - df.at[l, "Vout"]) / (df.at[l + 1, "Vin"] - df.at[l, "Vin"]))
            for l in range(1, len(derivatives)):
                if (np.abs(derivatives[l] - derivatives[l - 1]) > 0.1):
                    derivatives[l] = derivatives[l - 1]
            if (derivatives.index(max(derivatives)) - 10 < 0):
                avg_const = sum(derivatives[0:points]) / points
            else:
                avg_const = sum(derivatives[len(derivatives) - (points + 1):len(derivatives) - 1]) / points
            if ("Diode4" in labels[(sp_col * i) + j].split("_")):
                thresh_volt = 0.3
            else:
                thresh_volt = 0.6
            if (derivatives[len(derivatives) - 1] - derivatives[0] < 0):
                thresh_volt *= -1
            else:
                thresh_volt *= 1
            thresh_vout = percent * avg_const
            close = closest(derivatives, thresh_vout)
            index = derivatives.index(close)
            thresh_vin = df["Vin"][:-1][index]
            diff.append(np.abs(thresh_vin - thresh_volt))
            derivatives.clear()
    avgs.append(sum(diff) / len(diff))
    perc.append(percent)
    diff.clear()

min_thresh = min(avgs)
index_thresh = avgs.index(min_thresh)
perc_thresh = perc[index_thresh]

figure3, axis3 = plt.subplots(sp_row, sp_col)
avg_const = 0

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
        thresh_vout = perc_thresh * avg_const
        close = closest(derivatives, thresh_vout)
        index = derivatives.index(close)
        thresh_vin = df["Vin"][:-1][index]
        print("Threshold Voltage of " + labels[(sp_col * i) + j] + ": " + str(thresh_vin) + " V at " + str(round(100 * perc_thresh, 1)) + "%")
        axis3[i, j].axvline(x = thresh_vin)
        axis3[i, j].axhline(y = perc_thresh * avg_const)
        derivatives.clear()

figure3.suptitle("Numerical Differentiation: Thresholds Shown")
plt.tight_layout()
plt.savefig("Diff_vs_In_with_Thresholds.png")

plt.show()
