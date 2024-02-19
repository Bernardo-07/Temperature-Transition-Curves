import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares
import csv

def function(T, DBTT, C, D):
    US = 86 #-> input
    LS = 20 #-> input
    A = (LS + US)/2
    B = (US - LS)/2
    arg = (T - DBTT)/(C + (D*T))
    return A + B*np.tanh(arg)

data = '4340 34 10x10 - KV8.csv'
temperature = []
y = []

with open(data, mode='r') as file: #abre o arquivo no modo leitura
    file_csv = csv.reader(file) #cria uma variável para receber a leitura do arquivo
    next(file_csv) #pula o cabeçalho

    for line in file_csv: #itera sobre cada linha da variavel
        temperature.append(float(line[0]))
        y.append(float(line[1]))
        #extrai os dados transformanddo em float

print(temperature)
print(y)