import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

try:
    df = pd.read_csv("coincidence.csv", sep = ",", engine = "python")
except FileNotFoundError:
    print('"coincidence.csv" not found.')
    sys.exit(1)

maximum = max(df["Normalized count [/s]"])
HM = maximum / 2
nearest_above = (np.abs(maximum + HM)).argmax()
nearest_below = (np.abs(maximum - HM)).argmin()
FWHM = nearest_above - nearest_below
print(FWHM)

plt.plot(df["Angle [deg]"], df["Normalized count [/s]"], color = "b", label = "Data")
plt.xlabel("Angle [deg]")
plt.ylabel("Normalized Count [1/sec]")
plt.title("Normalized Count vs. Angle for Na-22 Coincidence")
plt.legend()
plt.show()
