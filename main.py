import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares
import csv

data = '4340 34 10x10 - KV8.csv'
temperature = []
y = []

with open(data, mode='r') as file:
    file_csv = csv.reader(file)

    for line in file_csv:
        temperature.append(line[0])
        y.append(line[1])

print(temperature)
print(y)