import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from scipy.optimize import curve_fit

def function(x, a, b, c):
    y = a/(x + np.abs(b))**c
    return y

files = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):
        files.append(sys.argv[i])
else:
    print("Incorrect format.")
    sys.exit(1)

frequencies = []
maxima = []
capacitances = [29.2, 76.3, 151.3, 220.5, 293.4, 357.5, 400.7]
cap_err = [0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1]

for f in files:
    try:
        df = pd.read_csv(f, sep = ",", header = None, engine = "python")
        df.columns = ["Frequency", "V_out/V_in", "V_in", "V_out"]
        quadratic_part = df.loc[(df["Frequency"] >= (df.loc[df["V_out/V_in"].idxmax()]["Frequency"] - 40.0)) & (df["Frequency"] <= (df.loc[df["V_out/V_in"].idxmax()]["Frequency"] + 40.0))]
        z = np.polyfit(quadratic_part["Frequency"], quadratic_part["V_out/V_in"], 2)
        f = np.poly1d(z)
        x_new = np.linspace(quadratic_part["Frequency"].iloc[0], quadratic_part["Frequency"].iloc[-1], 50)
        y_new = f(x_new)
        frequencies.append(x_new[y_new.argmax()])
        maxima.append(max(y_new))
    except FileNotFoundError:
        print("File " + f + " not found.")
        sys.exit(1)

parameters, covariance = curve_fit(function, capacitances, frequencies, p0 = [4000, 0.000001, 0.5])
print(parameters)
fit_x = np.arange(min(capacitances), max(capacitances), 0.01)
fit_y = function(fit_x, *parameters)

plt.scatter(capacitances, frequencies, color = "b", label = "Data")
plt.plot(fit_x, fit_y, color = "y", label = "Fit")
plt.xlabel("Capacitance [pF]")
plt.ylabel("Resonant Frequency [Hz]")
plt.title("Resonant Frequencies vs. Capcitance")
plt.legend()
plt.show()


# plt.errorbar(capacitances, frequencies, xerr = cap_err, fmt = ".", color = "b", label = "Data")
# frequencies.append(df.loc[df["V_out/V_in"].idxmax()]["Frequency"])
