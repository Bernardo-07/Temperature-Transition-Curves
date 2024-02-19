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

def erro(params, temperature, y):
    #calcula a diferença (ou erro) entre os dados observados e calculados
    DBTT, C, D = params
    Kv = function(temperature, DBTT, C, D)
    return y - Kv

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

#método de mínimos quadrados para achar o melhor valor para os parametros DBTT, C e D
for i in range(0, len(y)):
    initial_params = [-85, 35, 0.0256] #chute inicial
    result = least_squares(erro, initial_params, args=(temperature[i], y[i]))
    DBTT, C, D = result.x

print(DBTT)
print(C)
print(D)