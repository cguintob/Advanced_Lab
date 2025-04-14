import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

path1 = "~/Advanced_Lab/Spectroscopy/data/3-20/"
path2 = "~/Advanced_Lab/Spectroscopy/data/3-25/"
path3 = "~/Advanced_Lab/Spectroscopy/data/4-1/"

file1 = path1 + "3-20_computer_screen_50_10-7_10-7_350-900.txt"
file2 = path1 + "3-20_computer_night_50_10-7_10-7_350-700.txt"
file3 = path2 + "3-25_claire_laptop_100_10-6_10-7_350-700.txt"
file4 = path2 + "3-25_claire_laptop_warm_100_10-6_10-7_350-700.txt"
file5 = path2 + "3-25_bulb_blue_light_glass_10-5_10-7_350-700.txt"
file6 = path2 + "3-25_bulb_blue_light_on_10-5_10-7_350-700_take2.txt"
file7 = path3 + "4-1_sunlight_sunscreen_run1_10-6_10-6_300-700.txt"
file8 = path3 + "4-1_sunlight_sunscreen_run3_10-5_10-6_300-700.txt"

def wavelength_to_rgb(wavelength, gamma = 0.8):
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

block = 1.1
slide = 0.1
apert = 2
# g(x) = 0.523204x + 0.00508585
# We input the amount of free space (apert - block) into the equation to get the percent value of the intensity
coverages = [0.523204 * (apert - block) + 0.00508585, 0.523204 * (apert - (block + (4 * slide))) + 0.00508585]
sensitivities = [1, 10]

df1 = pd.read_csv(file3, sep = "\t", header = None, engine = "python")
df1.columns = ["Wavelength", "Intensity"]
df1["Wavelength"] += 23
df1.drop(df1[df1["Wavelength"] > 700].index, inplace = True)
# df1["Intensity"] *= (sensitivities[0]/coverages[0])
df1["Intensity"] /= df1["Wavelength"]

df2 = pd.read_csv(file4, sep = "\t", header = None, engine = "python")
df2.columns = ["Wavelength", "Intensity"]
df2["Wavelength"] += 23
df2.drop(df2[df2["Wavelength"] > 700].index, inplace = True)
# df2["Intensity"] *= (sensitivities[1]/coverages[1])
df2["Intensity"] /= df2["Wavelength"]

df3 = df2
df3["Intensity"] -= df1["Intensity"]
df3.dropna(axis = 0, inplace = True)

plt.figure()
for i in range(len(df3["Wavelength"])):
    plt.scatter(df3["Wavelength"][i], df3["Intensity"][i], color = [wavelength_to_rgb(df3["Wavelength"][i])], marker = ".")
plt.xlabel("Wavelength [nm]")
# plt.ylabel("Intensity Ratio")
# plt.ylim([0, 1])
# plt.title("Intensity Ratio vs. Wavelength")
plt.ylabel("Normalized Intensity Difference [V/nm]")
plt.ylabel("Intensity [V]")
plt.title("Normalized Intensity Difference vs. Wavelength")

plt.tight_layout()
plt.show()
