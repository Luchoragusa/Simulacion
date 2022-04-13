import random as ran
from cmath import sqrt
from xmlrpc.client import Boolean
import numpy as np # importando numpy
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
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

def graficarSaldos(m, band):
    if (band):
        for k in range(3):
            mSaldo = m[k]
            for i in range(len(mSaldo)):
                print("Corrida --> ", i)
                x = []
                for j in range(len(mSaldo[i])):
                    x.append(j+1)
                plt.plot(x,mSaldo[i])
            plt.xlabel("Numero de apuestas")
            plt.ylabel("Saldo")
            plt.title("Evolucion de saldo para " + str((k+1)*25) + " corridas")
            plt.show()
    else:
        for i in range(len(m)):
            print("Corrida --> ", i)
            x = []
            for j in range(len(m[i])):
                x.append(j+1)
            plt.plot(x,m[i])
        plt.xlabel("Numero de apuestas")
        plt.ylabel("Saldo")
        plt.title("Evolucion de saldo") 
        plt.show()

def graficarApuestas(m,  band):
    if (band):
        for k in range(3):
            mApuesta = m[k]
            for i in range(len(mApuesta)):
                print("Corrida --> ", i)
                x = []
                for j in range(len(mApuesta[i])):
                    x.append(j+1)
                plt.plot(x,mApuesta[i])
            plt.xlabel("Numero de apuestas")
            plt.ylabel("Valor de apuesta")
            plt.title("Evolucion de las apuestas para " + str((k+1)*25) + " corridas") 
            plt.show()
    else:
        for i in range(len(m)):
            print("Corrida --> ", i)
            x = []
            for j in range(len(m[i])):
                x.append(j+1)
            plt.plot(x,m[i])
        plt.xlabel("Numero de apuestas")
        plt.ylabel("Valor de apuesta")
        plt.title("Evolucion de las apuestas") 
        plt.show()

def graficarPromSaldos(m):
    mProm = []
    for i in range(len(m)):
        mTemp = m[i]
        mTemp2 = []
        for j in range(len(mTemp)):
            mTemp2.append(np.mean(mTemp[j]))
        mProm.append(np.mean(mTemp2))
    print("\nPromedio de saldos: ", mProm)

    eje_x = ["25 corridas", "50 corridas", "75 corridas"]
    eje_y = [mProm[0], mProm[1], mProm[2]]
    plt.axhline(y=5000, color = "red") # linea de saldo inicial
    plt.ylim([4000, 6500]) # esta ponderada la medicion
    plt.bar(eje_x, eje_y)
    plt.ylabel('Promedio de saldo resultante')
    plt.xlabel('Cantidad de corridas')
    plt.title('Promedio de saldo por cantidad de corridas')
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
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
            mSaldo.append(saldo_global)
        evolucionApuesta.append(matrizApuestas)
        evolucionSaldo.append(mSaldo) 

def tiradas(colorSeleccionado, dinero_apostado):
#Opcion 10 girar
    for i in range(5):
        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = saldoIni
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")

        while (band and contadorMG<= 25):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG] 
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
            mSaldo.append(saldo_global)
        evolucionApuesta.append(matrizApuestas)
        evolucionSaldo.append(mSaldo)

        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = saldoIni
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")
        while (band and contadorMG<= 50):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG] 
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
            mSaldo.append(saldo_global)
        evolucionApuesta1.append(matrizApuestas)
        evolucionSaldo1.append(mSaldo)

        matrizApuestas = []; matrizApuestas.append(dinero_apostado)
        saldo_global = saldoIni
        mSaldo = []; mSaldo.append(saldo_global)
        contadorMG = 0
        apuestaAct = matrizApuestas[contadorMG]
        band = True
        print("\n")
        while (band and contadorMG<= 75):
            nRandom = ran.randint (0,36)
            saldo_global -= apuestaAct # le descuento al salgoGlobal lo apostado
            contadorMG += 1
            if(nRandom in numerosRojos and colorSeleccionado == rojo) or (nRandom not in numerosRojos and colorSeleccionado == negro):
                saldo_global += apuestaAct*2
                matrizApuestas.append(dinero_apostado)
                apuestaAct = matrizApuestas[contadorMG]  
            else:
                if(apuestaAct*2 <= saldo_global):
                    matrizApuestas.append(apuestaAct*2)
                    apuestaAct = matrizApuestas[contadorMG]
                else:
                    band = False
            mSaldo.append(saldo_global)
        evolucionApuesta2.append(matrizApuestas)
        evolucionSaldo2.append(mSaldo) 

   

print("Bienvenido a la ruleta de la martin gala")
print("\n")
eleccion = int(input("\t###### MENU RULETA #######\n\t1. Jugar hasta agotar saldo\n\t2. Jugar 25, 50 y 75 tiradas\n\tElige: "))
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
    graficarSaldos(evolucionSaldo, False)

else:
    tiradas(colorSeleccionado, dinero_apostado)
    m = [evolucionApuesta, evolucionApuesta1, evolucionApuesta2]
    graficarApuestas(m, True)
    m = [evolucionSaldo, evolucionSaldo1, evolucionSaldo2]
    graficarSaldos(m, True)
    
    graficarPromSaldos(m)

