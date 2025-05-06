import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import pathlib

if (len(sys.argv) != 1):
    if (sys.argv[1].endswith(".txt")):
        f = sys.argv[1]
        title = pathlib.Path(f).stem
else:
    print("Incorrect format.")
    sys.exit(1)

df = pd.read_csv(f, sep = "\t", header = None, engine = "python")
df.dropna(axis = 1, inplace = True)
df.columns = ["Frequency", "Signal", "Temperature", "Unknown", "Excitation"]
f0 = df.loc[df["Signal"].argmax(), "Frequency"]
plt.scatter(df["Frequency"], df["Signal"], color = "b", marker = ".")
plt.axvline(x = f0, color = "g", label = "Resonant Frequency: {0} Hz".format(f0))
plt.title("Signal vs. Frequency for " + title)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Volts [V]")
plt.legend()

plt.savefig("plots/" + title + ".png")
plt.show()
