import random as ran
from heapq import heapify, heapreplace
from socketserver import UDPServer
from statistics import mean, quantiles
import matplotlib.pyplot as plt
import numpy as np # importando numpy
import networkx as nx


#===============================================================================================
#                         Funciones generadoras aleatoridad
#===============================================================================================
def rendom():
    n1 = ran.random()                               # Random float 0.0 <= x < 1.0
    return n1
def iuniform():
    n2 = ran.uniform(2.5, 10.0)                     # Random float 2.5 <= x <= 10.0
    return n2
def expo():
    n3 = ran.expovariate(1/5)                       # Intervalo entre llegadas con promedio de 5 segundos
    return n3
def ranrange():
    n4 = ran.randrange(10)                          # Integer de 0 a 9 inclusive
    return n4
def chois():
    n5 = ran.choice(['win', 'lose', 'draw'])        # Unico elemento aleatorio de una secuencia
    return n5
def barajarLista():
    deck = 'ace two three four'.split()             # barajar una lista 
    ran.shuffle(deck)
    n6 = deck
    return n6
def sampel(baraja):
    n7 = ran.sample(baraja, 3)      # 4 muestras sin reemplazo
    return n7
def init():
    n8 = ran.randint(1,10)                          # Entero aleatorio a <= x <= b
    return n8

#===============================================================================================
#                         Ejemplos de simulaciones usando aleatoridad
#===============================================================================================
def simulaciones():
# 6 giros de la rueda de la ruleta (muestreo ponderado con reemplazo)
    sim = ran.choices(['rojo', 'negro', 'verde'], [18, 18, 1], k=6)
    print(f"La muestra da {sim}")
# Repartir 20 cartas sin reemplazo de una baraja de 52 naipes, y determinar la proporción de naipes
# con un valor de diez: 10, sota, reina o rey.
    reparto = ran.sample(['dieces', 'cartas bajas'], counts=[16,36], k=20)
    c = reparto.count('dieces')/20
    print(f"Reparto {c}")
# Estimar la probabildiad de obtener 5 o más caras en 7 giros de una moneda sesgada que sale 'cara' el 60% de las veces
    def moneda():
        return ran.choices('HT', cum_weights=(0.60, 1.00), k=7).count('H') >= 5
    estimado = sum(moneda() for i in range(10_000)) / 10_000
    print(f"Probabilidad estimada: {estimado}")
# Probabilidad de que la mediana de 5 muestras esté en los dos cuartiles centrales
    def med():
        return 2_500 <= sorted(ran.choices(range(10_000), k=5))[2] < 7_500
    mediana = sum(med() for i in range(10_000)) / 10_000
    print(f"Probabilidad de la mediana: {mediana}")
# simulacion de tiempos de llegada y entrega de servicios para una cola de multiples servidores
    intervalo_llegada_promedio = 5.6
    promedio_servicio_tiempo = 15.0
    desvstand_tiempo_servicio = 3.5
    num_servidores = 3
    esperas = []
    tiempo_llegada = 0.0
    servidores = [0.0] * num_servidores     # tiempo en que cada servidor se vuelve disponible
    heapify(servidores)
    for i in range(1_000_000):
        tiempo_llegada += ran.expovariate(1.0 / intervalo_llegada_promedio)
        siguiente_server_disponible = servidores[0]
        espera = max(0.0, siguiente_server_disponible - tiempo_llegada)
        esperas.append(espera)
        duracion_servicio = max(0.0, ran.gauss(promedio_servicio_tiempo, desvstand_tiempo_servicio))
        servicio_completado = tiempo_llegada + espera + duracion_servicio
        heapreplace(servidores, servicio_completado)
    print(f"Espera: {mean(esperas):.1f} Maxima espera: {max(esperas):1f}")
    print("Cuartiles: ", [round(cu, 1) for cu in quantiles(esperas)])

def graficas():
    a = np.array([[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40], 
    [rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),
    rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),
    rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),
    rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom(),rendom()]])
    categorias = np.array([0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0])
    colormap = np.array(['r', 'c', 'b'])
    plt.scatter(a[0], a[1], s=100, c=colormap[categorias])
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Resultado aleatorio")
    plt.title("Evaluacion de ran.random()")
    plt.show()
    a = np.array([[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40], 
    [iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),
    iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),
    iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),
    iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),iuniform(),
    iuniform(),iuniform(),iuniform(),iuniform()]])
    categorias = np.array([0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0])
    colormap = np.array(['g', 'm', 'y'])
    plt.scatter(a[0], a[1], s=100, c=colormap[categorias])
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Resultado aleatorio")
    plt.title("Evaluacion de ran.uniform(1,10)")
    plt.show()
#Ejemplo de jugar al Truco: en una mano de 3 jugadores, qué cartas pueden salir dentro de la baraja de 1 a 12 cartas del juego para c/u
    x = []; y = []; baraja = [1,2,3,4,5,6,7,10,11,12]; rangoy = np.arange(1,13,1); 
    for i in range(3):
        cartas = sampel(baraja)    
        x.append(i+1)
        y.append(cartas)
        plt.plot(x,y, marker='o')
    plt.xlabel("Orden de las cartas")
    plt.ylabel("Resultado aleatorio de valores de cartas")
    plt.title("Evaluacion de ran.sample()")
    plt.xticks(x)
    plt.yticks(rangoy)
    plt.show()

#Método de la parte media del cuadrado de Jon Von Neuman
def middleSquare():
    semilla = int(input("Ingrese un numero de 4 digitos: "))
    numero = semilla
    historial = []
    cont = 0
    while numero not in historial:
        cont += 1
        historial.append(numero)
        cuad = numero*numero
        numero = int(str(cuad).zfill(8)[2:6])      #zfill agrega relleno de ceros
        print(f"#{cont}:\nvalor = '{cuad}', new seed = {numero}")
    print(f"Empezamos con '{semilla}', hemos repetido el proceso '{cont}'")

#middleSquare()

def randu():
    n = 150000
    x = [[0],[n]]; u = [[0],[n]]
    x[1] = 4798373
    u[1] = x[1] / (2^31 - 1)
    for i in range(2,n):
        x[i] = ((2 ^ 16 + 3) * x[i-1]) % (2 ^ 31)
        u[i] = x[i] / (2 ^ 31)
    plt.plot(x,u)
    plt.show()
#randu()

