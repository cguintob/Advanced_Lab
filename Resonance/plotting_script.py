import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

if (len(sys.argv) != 1):
    if (sys.argv[i].endswith(".txt")):
        f = sys.argv[i]
    else:
        continue
else:
    print("Incorrect format.")
    sys.exit(1)

df = pd.read_csv(f, sep = "\t", header = None, engine = "python")
df.columns = ["Frequency", "Signal", "Temperature", "Unknown", "Excitation"]
plt.scatter(df["Frequency"], df["Signal"], color = "b", marker = ".")
plt.title("Signal vs. Frequency")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Volts [V]")

plt.show()
