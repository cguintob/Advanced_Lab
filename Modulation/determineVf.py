import numpy as np

# Step 1: Read the file into a NumPy array
# Make sure the file path is correct and the file is formatted properly
file_path = "slopedDD/wSlope_Diode4_dir2_200s"

data = np.loadtxt(file_path)  # Assumes a whitespace-delimited file

# Step 2: Remove highly discontinuous data points in the slope (third column)
# Calculate the difference in consecutive values of the third column (slope)
slope_diff = np.diff(data[2:, 2])
threshold_slope_diff = np.mean(np.abs(slope_diff)) + 2 * np.std(np.abs(slope_diff))
print(threshold_slope_diff)

# Identify indices where the slope difference is below the threshold
continuous_indices = np.where(np.abs(slope_diff) <= threshold_slope_diff)[0]
continuous_indices = np.append(continuous_indices, continuous_indices[-1] + 1)  # Include the last point

# Filter the data to keep only continuous points
print(len(data[:, 0]))
filtered_data_continuous = data[continuous_indices]
print(len(filtered_data_continuous[:, 0]))

# Step 3: Find the average slope on the resistor-like extremes
filtered_data = filtered_data_continuous[(np.abs(filtered_data_continuous[:, 0]) > 1.0) & (np.abs(filtered_data_continuous[:, 2]) > 0.5)]
slope_average = np.mean(filtered_data[:, 2])
print("slope average ", slope_average)

# Step 4: Determine scan direction based on filtered_data
if np.all(filtered_data[:, 0] < 0):
    data_sorted = filtered_data_continuous[np.argsort(filtered_data_continuous[:, 0])]  # Sort from negative to positive
elif np.all(filtered_data[:, 0] > 0):
    data_sorted = filtered_data_continuous[np.argsort(filtered_data_continuous[:, 0])[::-1]]  # Sort from positive to negative
else:
    data_sorted = filtered_data_continuous  # No specific order if mixed

threshold = 0.1 * slope_average
for i, slope in enumerate(data_sorted[:, 2]):
    if abs(slope - slope_average) > threshold:
        V_i = data_sorted[i, 0]
        print(f"At index {i}, slope {slope} differs by more than 5% of the average. V_i = {V_i}")
        break  # Exit the loop after finding the first occurrence
