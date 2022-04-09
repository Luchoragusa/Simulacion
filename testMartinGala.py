import random as ran
from cmath import sqrt
from xmlrpc.client import Boolean
import numpy as np # importando numpy
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
from scipy import stats # importando scipy.stats

apuesta_minima_ruleta = 5
rojo = "Rojo"
negro = "Negro"
evolucionApuesta = []
evolucionSaldo = []

evolucionApuesta1 = []
evolucionSaldo1 = []

evolucionApuesta2 = []
evolucionSaldo2 = []

numerosRojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]


# Definir apuesta por columna y por docena, ademas hacer que se pueda apostar por muchos a la vez
# Modificar la opcion 1 para que sea solo numero, y que se pueden apostar a varias opciones

menu = """###### MENU RULETA #######
1. JUGAR
2. SALIR
Elige: """

def solicitarDineroRuleta():
    dinero_apostado = 0
    dinero_apostado = float(input(f"\n\t¿Cuanto apostás a la martin gala? Debe ser al menos '{apuesta_minima_ruleta}' pesos, y no debe superar el saldo: "))
    band = True
    while band:
        if(dinero_apostado >= apuesta_minima_ruleta ):
            band = False
        else:
            dinero_apostado = float(input(f"Valor no valido, ingresa una apuesta valida: "))
    return dinero_apostado

def pedirNumero():
    numero = int(input("Elige un numero entre 0 y 36: "))
    band = True
    while (band): 
        if 0 < numero < 36:
            band = False
            return numero
        else:
            band = True

def graficarSaldos(evolucionSaldo):
    for i in range(len(evolucionSaldo)):
        print("Corrida --> ", i)
        x = []
        for j in range(len(evolucionSaldo[i])):
            x.append(j+1)
        plt.plot(x,evolucionSaldo[i])
    plt.xlabel("Numero de apuestas")
    plt.ylabel("Saldo")
    plt.title("Evolucion de saldo") 
    plt.show()

def graficarApuestas(evolucionApuesta):
    for i in range(len(evolucionApuesta)):
        print("Corrida --> ", i)
        x = []
        for j in range(len(evolucionApuesta[i])):
            x.append(j+1)
        plt.plot(x,evolucionApuesta[i])
    plt.xlabel("Numero de apuestas")
    plt.ylabel("Valor de apuesta")
    plt.title("Evolucion de las apuestas") 
    plt.show()

def agotarSaldo(colorSeleccionado, dinero_apostado):
#Opcion 10 girar
    for i in range(5):
        matrizApuestas = []
        saldo_global = 500 #El saldo con el que se inicia
        mSaldo = []
        mSaldo.append(saldo_global)
        matrizApuestas.append(dinero_apostado)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")
        while (band):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG]
                print("Apostaste: ", apuestaAct, " y ganaste, el saldo global es: ", saldo_global)    
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
                print("Apostaste: ", apuestaAct, " y Perdiste, el saldo global es: ", saldo_global) 
            mSaldo.append(saldo_global)
        print("Te quedaste sin saldo")
        evolucionApuesta.append(matrizApuestas)
        evolucionSaldo.append(mSaldo) 

def tiradas(colorSeleccionado, dinero_apostado):
#Opcion 10 girar
    for i in range(5):
        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = 500 
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")

        while (band and contadorMG<= 10):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG]
                print("Apostaste: ", apuestaAct, " y ganaste, el saldo global es: ", saldo_global)    
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
                print("Apostaste: ", apuestaAct, " y Perdiste, el saldo global es: ", saldo_global) 
            mSaldo.append(saldo_global)
        print("Te quedaste sin saldo")
        evolucionApuesta.append(matrizApuestas)
        evolucionSaldo.append(mSaldo)

        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = 500 
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")
        while (band and contadorMG<= 20):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG]
                print("Apostaste: ", apuestaAct, " y ganaste, el saldo global es: ", saldo_global)    
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
                print("Apostaste: ", apuestaAct, " y Perdiste, el saldo global es: ", saldo_global) 
            mSaldo.append(saldo_global)
        print("Te quedaste sin saldo")
        evolucionApuesta1.append(matrizApuestas)
        evolucionSaldo1.append(mSaldo)

        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = 500 
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")
        while (band and contadorMG<= 30):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG]
                print("Apostaste: ", apuestaAct, " y ganaste, el saldo global es: ", saldo_global)    
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
                print("Apostaste: ", apuestaAct, " y Perdiste, el saldo global es: ", saldo_global) 
            mSaldo.append(saldo_global)
        print("Te quedaste sin saldo")
        evolucionApuesta2.append(matrizApuestas)
        evolucionSaldo2.append(mSaldo) 

   

print("Bienvenido a la ruleta de la martin gala")
print("\n")
eleccion = int(input("\t###### MENU RULETA #######\n\t1. Jugar hasta agotar saldo\n\t2. Jugar 20 tiradas\n\tElige: "))
print("\n")
colorSeleccionado = ""
dinero_apostado = solicitarDineroRuleta()
color_eleccion_usuario = input("\t1.Rojo\n\t2.Negro\n\tElige: ") 
if color_eleccion_usuario == "1":
    colorSeleccionado = rojo
else: 
    colorSeleccionado = negro

if eleccion == 1:
    agotarSaldo(colorSeleccionado, dinero_apostado)
else:
    tiradas(colorSeleccionado, dinero_apostado)
    graficarSaldos(evolucionSaldo1)
    graficarApuestas(evolucionApuesta1)
    graficarSaldos(evolucionSaldo2)
    graficarApuestas(evolucionApuesta2)


graficarSaldos(evolucionSaldo)
graficarApuestas(evolucionApuesta)
