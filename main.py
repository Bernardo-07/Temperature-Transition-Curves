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
    y_fit = function(temperature, DBTT, C, D, US, LS)
    return y - y_fit

def choose_file():
    file_path = filedialog.askopenfilename(title="Selecione o Arquivo", filetypes=[("Arquivos CSV", "*.csv")])
    return file_path

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    return file_path

def plot(temperature, y, y_fit, aux):
    plt.title('Gráfico da Tangente Hiperbólica Assimétrica')
    plt.scatter(temperature, y, color="r", marker="o", edgecolor='black')
    plt.plot(temperature, y_fit, color="b")
    
    plt.xlabel('Temperature (°C)')
    if aux == 1:
        plt.ylabel('Kv (J)')
    elif aux == 2:
        plt.ylabel('LE (mm)')
    elif aux == 3:
        plt.ylabel('SFA (%)')
        
    plt.xlim(-200, 100) 
    plt.ylim(0, 100)
    #intersec = np.interp(DBTT, temperature, y)
    intersec = function(DBTT, DBTT, C, D, US, LS)
    plt.plot([DBTT, DBTT], [0, intersec], 'k--', lw=1, label = 'DBTT') #[xi, xf], [yi, yf]

    '''x_max = max(temperature)
    y_max = max(max(y), max(y_fit))
    legend_x = x_max * 0.7
    legend_y = y_max * 0.2
    plt.text(legend_x, legend_y , f'DBTT = {DBTT:.2f}\nC = {C:.2f}\nD = {D:.4f}', ha='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.6'))'''
    
    plt.legend(loc='upper left', edgecolor='black')
    plt.grid(True)

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
            
aux = int(input("\nEscolha um dos seguintes parâmetros para o eixo das ordenadas:\n1 - Kv (J)\n2 - LE (mm)\n3 - SFA (%)\nDigite o número associado: "))

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

print("\n")
print(DBTT)
print(C)
print(D)

y_fit = [None] * len(y)
for i in range(0, len(y)):
    y_fit[i] = function(temperature[i], DBTT, C, D, US, LS)

plot(temperature, y, y_fit, aux)
plt.show()

answer = input("\nDeseja salvar o gráfico? (sim/nao): ")

if answer == 'sim':

    plot(temperature, y, y_fit, aux)
    plt.savefig(save_file())
    
    print("Gráfico salvo")

elif answer == 'nao':
    print("Gráfico não foi salvo")

else:
    print("Resposta inválida")
