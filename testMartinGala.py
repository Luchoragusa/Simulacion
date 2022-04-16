import random as ran
from cmath import sqrt
from xmlrpc.client import Boolean
import numpy as np # importando numpy
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import alphas, col 
from scipy import stats # importando scipy.stats

saldoIni = 5000
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

def graficarSaldos(m, band):
    if (band):
        for k in range(3):
            mSaldo = m[k]
            for i in range(len(mSaldo)):
                x = []
                for j in range(len(mSaldo[i])):
                    x.append(j+1)
                plt.plot(x,mSaldo[i])
            plt.xlabel("Numero de apuestas")
            plt.ylabel("Saldo")
            plt.title("Evolucion de saldo para " + str((k+1)*25) + " jugadas")
            plt.axhline(y=saldoIni, color = "red") # linea de saldo inicial
            plt.grid()
            plt.show()
    else:
        for i in range(len(m)):
            x = []
            for j in range(len(m[i])):
                x.append(j+1)
            plt.plot(x,m[i])
        plt.xlabel("Numero de apuestas")
        plt.ylabel("Saldo")
        plt.title("Evolucion de saldo") 
        plt.axhline(y=saldoIni, color = "red") # linea de saldo inicial
        plt.grid()
        plt.show()

def graficarApuestas(m,  band):
    if (band):
        for k in range(3):
            mApuesta = m[k]
            for i in range(len(mApuesta)):
                x = []
                for j in range(len(mApuesta[i])):
                    x.append(j+1)
                plt.plot(x,mApuesta[i])
            plt.xlabel("Numero de apuestas")
            plt.ylabel("Valor de apuesta")
            plt.title("Evolucion de las apuestas para " + str((k+1)*25) + " jugadas")
            plt.grid()  
            plt.show()
    else:
        for i in range(len(m)):
            x = []
            for j in range(len(m[i])):
                x.append(j+1)
            plt.plot(x,m[i])
        plt.xlabel("Numero de apuestas")
        plt.ylabel("Valor de apuesta")
        plt.title("Evolucion de las apuestas")
        plt.grid()
        plt.show()

def graficarPromSaldos(m):
    mProm = []
    for i in range(len(m)):
        mTemp = m[i]
        mTemp2 = []
        for j in range(len(mTemp)):
            mTemp2.append(np.mean(mTemp[j]))
        mProm.append(np.mean(mTemp2))
    eje_x = ["25 jugadas", "50 jugadas", "75 jugadas"]
    eje_y = [mProm[0], mProm[1], mProm[2]]
    plt.axhline(y=saldoIni, color = "red") # linea de saldo inicial
    plt.bar(eje_x, eje_y)
    plt.ylabel('Promedio de saldo resultante')
    plt.xlabel('Cantidad de jugadas')
    plt.title('Promedio de saldo por cantidad de jugadas')
    plt.grid()
    plt.show()

def graficarFR(mDato, band):
    if (band):
        for l in range(3):
            evolucionApuesta = mDato[l]
            mApuesta = []
            mCantApuesta=[]
            c = 0
            for i in range(len(evolucionApuesta)):
                m = evolucionApuesta[i]
                for j in range(len(m)): # recorro cada apuesta
                    if m[j] in mApuesta: # me fijo si la apuesta ha se hizo
                        for k in range(len(mApuesta)): # recorro la matriz de apuestas para ver en q posicion esta guardada la apuesta
                            if mApuesta[k] == m[j]:
                                mCantApuesta[k] += 1 # le sumo uno en la posicion que corresponde de la matriz de apuesta
                    else: # si no esta agrego la apuesta y le agg 1 en la cantidad
                        mApuesta.append(m[j])
                        mCantApuesta.append(1)
                    c += 1
            for i in range(len(mCantApuesta)): # obtengo la FR de cantidad de apuestas
                mCantApuesta[i] = mCantApuesta[i]/c  
                mApuesta[i] = str(mApuesta[i])
            plt.bar(mApuesta, mCantApuesta, alpha = 0.75, width= 0.25)
            plt.title("Frecuencia relativa por apuesta para " + str((l+1)*25) + " jugadas")
            plt.xlabel('Valor de apuesta')
            plt.ylabel('Frecuencia jugadas')
            plt.grid()
            plt.show()
    else:
        mApuesta = []
        mCantApuesta=[]
        c = 0
        for i in range(len(mDato)):
            m = mDato[i]
            for j in range(len(m)): # recorro cada apuesta
                if m[j] in mApuesta: # me fijo si la apuesta ha se hizo
                    for k in range(len(mApuesta)): # recorro la matriz de apuestas para ver en q posicion esta guardada la apuesta
                        if mApuesta[k] == m[j]:
                            mCantApuesta[k] += 1 # le sumo uno en la posicion que corresponde de la matriz de apuesta
                else: # si no esta agrego la apuesta y le agg 1 en la cantidad
                    mApuesta.append(m[j])
                    mCantApuesta.append(1)
                c += 1
        for i in range(len(mCantApuesta)): # obtengo la FR de cantidad de apuestas
            mCantApuesta[i] = mCantApuesta[i]/c  
            mApuesta[i] = str(mApuesta[i])
        plt.bar(mApuesta, mCantApuesta, alpha = 0.75, width= 0.25)
        plt.tittle('Frecuencia relativa por apuesta')
        plt.xlabel('Valor de apuesta')
        plt.ylabel('Frecuencia relativa')
        plt.grid()
        plt.show()

def agotarSaldo(colorSeleccionado, dinero_apostado):
#Opcion 10 girar
    for i in range(5):
        matrizApuestas = []
        saldo_global = saldoIni #El saldo con el que se inicia
        mSaldo = []
        mSaldo.append(saldo_global)
        matrizApuestas.append(dinero_apostado)
        contadorMG = 0
        band = True
        while (band):
            nRandom = ran.randint (0,36)
            saldo_global -= matrizApuestas[contadorMG] # le descuento al salgoGlobal lo apostado
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += matrizApuestas[contadorMG]*2
                matrizApuestas.append(matrizApuestas[0]) 
            else:
                if(matrizApuestas[contadorMG]*2 <= saldo_global):
                    matrizApuestas.append(matrizApuestas[contadorMG]*2)
                else:
                    band = False 
            mSaldo.append(saldo_global)
            contadorMG += 1
        evolucionApuesta.append(matrizApuestas)
        evolucionSaldo.append(mSaldo) 

def tiradas(colorSeleccionado, dinero_apostado):
#Opcion 10 girar
    for i in range(5):
        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = saldoIni #El saldo con el que se inicia
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        band = True

        while (band and contadorMG<= 25):
            nRandom = ran.randint (0,36)
            saldo_global -= matrizApuestas[contadorMG] # le descuento al salgoGlobal lo apostado
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += matrizApuestas[contadorMG]*2
                matrizApuestas.append(matrizApuestas[0]) 
            else:
                if(matrizApuestas[contadorMG]*2 <= saldo_global):
                    matrizApuestas.append(matrizApuestas[contadorMG]*2)
                else:
                    band = False 
            mSaldo.append(saldo_global)
            contadorMG += 1
        evolucionApuesta.append(matrizApuestas)
        evolucionSaldo.append(mSaldo)

        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = saldoIni #El saldo con el que se inicia
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        band = True

        while (band and contadorMG<= 50):
            nRandom = ran.randint (0,36)
            saldo_global -= matrizApuestas[contadorMG] # le descuento al salgoGlobal lo apostado
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += matrizApuestas[contadorMG]*2
                matrizApuestas.append(matrizApuestas[0]) 
            else:
                if(matrizApuestas[contadorMG]*2 <= saldo_global):
                    matrizApuestas.append(matrizApuestas[contadorMG]*2)
                else:
                    band = False 
            mSaldo.append(saldo_global)
            contadorMG += 1
        evolucionApuesta1.append(matrizApuestas)
        evolucionSaldo1.append(mSaldo)

        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = saldoIni #El saldo con el que se inicia
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        band = True

        while (band and contadorMG<= 75):
            nRandom = ran.randint (0,36)
            saldo_global -= matrizApuestas[contadorMG] # le descuento al salgoGlobal lo apostado
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += matrizApuestas[contadorMG]*2
                matrizApuestas.append(matrizApuestas[0]) 
            else:
                if(matrizApuestas[contadorMG]*2 <= saldo_global):
                    matrizApuestas.append(matrizApuestas[contadorMG]*2)
                else:
                    band = False 
            mSaldo.append(saldo_global)
            contadorMG += 1
        evolucionApuesta2.append(matrizApuestas)
        evolucionSaldo2.append(mSaldo) 

   

print("Bienvenido a la ruleta de la martin gala")
print("\n")
eleccion = int(input("\t###### MENU RULETA #######\n\t1. Jugar hasta agotar saldo\n\t2. Jugar 25, 50 y 75 jugadas\n\tElige: "))
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
    graficarApuestas(evolucionApuesta, False)
    graficarFR(evolucionApuesta, False)
    graficarSaldos(evolucionSaldo, False)

else:
    tiradas(colorSeleccionado, dinero_apostado)
    m = [evolucionApuesta, evolucionApuesta1, evolucionApuesta2]
    graficarApuestas(m, True)
    graficarFR(m, True)
    m = [evolucionSaldo, evolucionSaldo1, evolucionSaldo2]
    graficarSaldos(m, True)
    graficarPromSaldos(m)

