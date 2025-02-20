import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import re

files = []
labels = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):
        if (sys.argv[i].endswith(".csv")):
            files.append(sys.argv[i])
            name = re.split(r"[/.]+", sys.argv[i])
            labels.append(name[1])
        else:
            print("Incorrect format.")
            sys.exit(1)
            
colors = ["cyan", "green", "yellow", "magenta", "blue", "orange", "purple", "black", "dimgray"]

figure, axis = plt.subplots(3, 3)

for i in range(len(files)):
    df = pd.read_csv(files[i], sep = ",", engine = "python")
    if (i < 3):
        axis[0, i].plot(df["Vin"], df["Vout"], colors[i])
        axis[0, i].set_xlabel("Vin", fontsize = 8)
        axis[0, i].set_ylabel("Vout", fontsize = 8)
        axis[0, i].set_xlim(min(df["Vin"]), max(df["Vin"]))
        axis[0, i].set_ylim(min(df["Vout"]), max(df["Vout"]))
        axis[0, i].set_xticks(np.arange(min(df["Vin"].astype(float)), max(df["Vin"].astype(float)) + 1, (max(df["Vin"].astype(float)) - min(df["Vin"].astype(float))) / 2))
        axis[0, i].set_yticks(np.arange(min(df["Vout"].astype(float)), max(df["Vout"].astype(float)) + 1, (max(df["Vout"].astype(float)) - min(df["Vout"].astype(float))) / 2))
        axis[0, i].tick_params(labelsize = 5)
        axis[0, i].set_title(labels[i], fontsize = 8)
        axis[0, i].tick_params(axis = "y", rotation = 90)
        axis[0, i].set_title(labels[i], fontsize = 8)
    elif (i >= 3 and i < 6):
        axis[1, i - 3].plot(df["Vin"], df["Vout"], colors[i])
        axis[1, i - 3].set_xlabel("Vin", fontsize = 8)
        axis[1, i - 3].set_ylabel("Vout", fontsize = 8)
        axis[1, i - 3].set_xlim(min(df["Vin"]), max(df["Vin"]))
        axis[1, i - 3].set_ylim(min(df["Vout"]), max(df["Vout"]))
        axis[1, i - 3].set_xticks(np.arange(min(df["Vin"].astype(float)), max(df["Vin"].astype(float)) + 1, (max(df["Vin"].astype(float)) - min(df["Vin"].astype(float))) / 2))
        axis[1, i - 3].set_yticks(np.arange(min(df["Vout"].astype(float)), max(df["Vout"].astype(float)) + 1, (max(df["Vout"].astype(float)) - min(df["Vout"].astype(float))) / 2))
        axis[1, i - 3].tick_params(labelsize = 5)
        axis[1, i - 3].set_title(labels[i], fontsize = 8)
        axis[1, i - 3].tick_params(axis = "y", rotation = 90)
        axis[1, i - 3].set_title(labels[i], fontsize = 8)
    else:
        axis[2, i - 6].plot(df["Vin"], df["Vout"], colors[i])
        axis[2, i - 6].set_xlabel("Vin", fontsize = 8)
        axis[2, i - 6].set_ylabel("Vout", fontsize = 8)
        axis[2, i - 6].set_xlim(min(df["Vin"]), max(df["Vin"]))
        axis[2, i - 6].set_ylim(min(df["Vout"]), max(df["Vout"]))
        axis[2, i - 6].set_xticks(np.arange(min(df["Vin"].astype(float)), max(df["Vin"].astype(float)) + 1, (max(df["Vin"].astype(float)) - min(df["Vin"].astype(float))) / 2))
        axis[2, i - 6].set_yticks(np.arange(min(df["Vout"].astype(float)), max(df["Vout"].astype(float)) + 1, (max(df["Vout"].astype(float)) - min(df["Vout"].astype(float))) / 2))
        axis[2, i - 6].tick_params(labelsize = 5)
        axis[2, i - 6].set_title(labels[i], fontsize = 8)
        axis[2, i - 6].tick_params(axis = "y", rotation = 90)
        axis[2, i - 6].set_title(labels[i], fontsize = 8)

figure.suptitle("Output vs. Input Voltages for Diodes and Resistor")
plt.tight_layout()
plt.show()

'''
y_hor = []
x_hor = np.linspace(df["Input"].iloc[0], df["Input"].iloc[-1], len(df["Input"]))
for i in range(len(x_hor)):
    y_hor.append(0)
plt.plot(x_hor, y_hor, color = "r")
'''
