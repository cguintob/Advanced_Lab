import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

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

live_times = [250.46, 307428.9] 
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
    except FileNotFoundError:
        print("Couldn't find file.")
        sys.exit(1)
