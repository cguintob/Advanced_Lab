import sys
import os
import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import traceback
# import optparse
# import time
# import logging

def wavelength_to_rgb(wavelength, gamma = 0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).
    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    return (R/255, G/255, B/255)


files= []
try:
    for i in range(1, len(sys.argv)):
        files.append(sys.argv[i])
except FileNotFoundError:
    print("Data file not found.")
    sys.exit(1)

titles = []
for i in range(len(files)):
    root, ext = os.path.splitext(files[i])
    titles.append(root)

for i in range(len(files)):
    df = pd.read_csv(files[i], sep = "\t", header = None, engine = "python")
    df.columns = ["Wavelength", "Intensity"]
    # df["Wavelength"] += 23
    df.drop(df[df["Wavelength"] > 700].index, inplace = True)
    plt.figure()
    for j in range(len(df["Wavelength"])):
        plt.scatter(df["Wavelength"][j], df["Intensity"][j], color = [wavelength_to_rgb(df["Wavelength"][j])], marker = ".")
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Intensity")
    plt.ylim([0, None])
    plt.title(titles[i])

'''
# Claire iPhone

file1 = "3-25_claire_phone_100_10-6_10-7_350-700.txt"
file2 = "3-25_claire_phone_100_10-6_10-7_560-700.txt"

df1 = pd.read_csv(file1, sep = "\t", header = None, engine = "python")
df1.columns = ["Wavelength", "Intensity"]
df1["Wavelength"] += 23
df1["Intensity"].loc[df1["Wavelength"] > (560 + 23)] = 0
# df1["Intensity"].loc[df1["Wavelength"] > 560] = 0
df1.set_index("Wavelength", inplace = True)
df2 = pd.read_csv(file2, sep = "\t", header = None, engine = "python")
df2.columns = ["Wavelength", "Intensity"]
df2["Wavelength"] += 23
df2.set_index("Wavelength", inplace = True)
df3 = df1
df3["Intensity"].loc[df3.index > (560 + 23)] += df2["Intensity"]
# df3["Intensity"].loc[df3.index > 560] += df2["Intensity"]
df3.reset_index(inplace = True)
for j in range(len(df3["Wavelength"])):
    plt.scatter(df3["Wavelength"][j], df3["Intensity"][j], color = [wavelength_to_rgb(df3["Wavelength"][j])], marker = ".")
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity")
plt.ylim([0, None])
plt.title("Claire iPhone")
'''

plt.show()
