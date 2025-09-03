import os
from tqdm import tqdm
import numpy as np
from scipy.stats import pareto
import statistics


ftp_config = {}
ftp_config['files_directory'] = '../data/ftp/'

def increase_std(data, target_std):

    # Calculate the mean of the data
    mean = np.mean(data)

    # Check if the target standard deviation is achievable
    current_std = np.std(data)
    if target_std < current_std:
        print("Target standard deviation is lower than current standard deviation. No modification required.")
        return data
    elif target_std == current_std:
        print("Target standard deviation is the same as current standard deviation. No modification required.")
        return data

    # Calculate the scaling factor to reach the target standard deviation
    scale_factor = np.sqrt((target_std**2) / (current_std**2))

    # Create a copy of the data to avoid modifying the original list
    data_copy = data.copy()

    # Split the data into two halves (you can adjust this split ratio if desired)
    half_length = int(len(data) / 2)
    first_half, second_half = data_copy[:half_length], data_copy[half_length:]

    # Increase the spread of one half of the data by scaling it further from the mean
    second_half = mean + scale_factor * abs(second_half - mean)

    # Combine the modified halves back together
    data_copy = np.concatenate((first_half, second_half))

    return data_copy

def nudge_median(data, target_median):

    # Sort the data to maintain order
    sorted_data = sorted(data)

    # Calculate the current median
    current_median = np.median(sorted_data)

    # Check if the target median is achievable within the data range
    if target_median < sorted_data[0] or target_median > sorted_data[-1]:
        print("Target median is not achievable while maintaining order.")
        return sorted_data

    # Determine the direction to nudge the median
    direction = 1 if target_median > current_median else -1

    # Iterate through the sorted data, inserting new elements strategically
    modified_data = []
    for num in sorted_data:
        modified_data.append(num)
        # Insert a new element with a nudge value closer to the target median
        if direction > 0:
            modified_data.append((num + target_median) / 2)
        else:
            modified_data.append((num + current_median) / 2)

    return modified_data

if __name__ == "__main__":
    mean = 362.40
    std = 12470
    median = 1.17

    file_sizes = pareto.rvs(1.41, size=500)
    file_sizes = [abs(f) for f in file_sizes]
    file_sizes = nudge_median(file_sizes, median)
    file_sizes = increase_std(file_sizes, std)
    file_sizes = nudge_median(file_sizes, median)

    print(statistics.stdev(file_sizes))
    print(statistics.median(file_sizes))
    print(file_sizes)

    file_sizes = [int(f*1024) for f in file_sizes]

    max_file_size = 0
    for size in file_sizes:
        if size > max_file_size:
            max_file_size = size
    charone = 'x'
    file_content = charone * max_file_size

    if not os.path.exists(ftp_config['files_directory']):
        os.makedirs(ftp_config['files_directory'])

    for size in tqdm(file_sizes):
        filename = 'p' + str(size) + '.txt'
        if not os.path.exists(ftp_config['files_directory']+filename):
            f = open(ftp_config['files_directory']+filename, "w")
            f.write(file_content[:size])
            f.close()