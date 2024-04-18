import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares
from tkinter import filedialog
import csv

def function(T, DBTT, C, D, US, LS):
    #US = 86.5 input
    #LS = 20 input
    A = (LS + US)/2
    B = (US - LS)/2
    arg = (T - DBTT)/(C + (D*T))
    return A + B*np.tanh(arg)

def error(params, temperature, y, US, LS):
    #calcula a diferença (ou erro) entre os dados observados e calculados
    DBTT, C, D = params
    Kv = function(temperature, DBTT, C, D, US, LS)
    return y - Kv

def choose_file():
    file_path = filedialog.askopenfilename(title="Selecione o Arquivo", filetypes=[("Arquivos CSV", "*.csv")])
    return file_path

data = choose_file()

temperature = []
y = []

with open(data, mode='r') as file: #abre o arquivo no modo leitura
    file_csv = csv.reader(file) #cria uma variável para receber a leitura do arquivo
    next(file_csv) #pula o cabeçalho

    for line in file_csv: #itera sobre cada linha da variavel
        temperature.append(float(line[0]))
        y.append(float(line[1]))
        #extrai os dados transformanddo em float

for i in range(0, len(temperature)):
    for j in range(0, len(temperature)-i-1):
        if temperature[j] > temperature[j+1]:
            # Trocar os elementos se estiverem fora de ordem
            temperature[j], temperature[j+1] = temperature[j+1], temperature[j]
            y[j], y[j+1] = y[j+1], y[j]

print("\nDigite o valor do chute inicial para os seguintes parâmetros")
DBTT = float(input("DBTT: "))
C = float(input("C: "))
D = float(input("D: "))

US = float(input("Upper Shelf: "))
LS = float(input("Lower Shelf: "))


#método de mínimos quadrados para achar o melhor valor para os parametros DBTT, C e D
initial_params = [DBTT, C, D] #[-85, 35, 0.0256] -> chute inicial 
result = least_squares(error, initial_params, args=(np.array(temperature), np.array(y), np.array(US), np.array(LS)))
DBTT, C, D = result.x

print(DBTT)
print(C)
print(D)

Kv = [None] * len(y)
for i in range(0, len(y)):
    Kv[i] = function(temperature[i], DBTT, C, D, US, LS)

plt.title('Gráfico da Tangente Hiperbólica Assimétrica')
plt.scatter(temperature, y, color="r", marker="D")
plt.plot(temperature, Kv)
plt.xlabel('T (°C)')
plt.ylabel('Kv (J)')
plt.text(50, 20, f'DBTT = {DBTT:.2f}\nC = {C:.2f}\nD = {D:.4f}', ha='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.6'))
plt.grid(True)

bool = input("Deseja salvar o gráfico? (sim/nao): ")

if bool == 'sim' or 's':
    
    file_path2 = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    plt.savefig(file_path2)
    print("Gráfico salvo")

elif bool == 'não' or 'nao' or 'n':
    print("Gráfico não foi salvo")

else:
    print("Resposta inválida")

plt.show()