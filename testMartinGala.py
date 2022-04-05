import random as ran
from cmath import sqrt
from xmlrpc.client import Boolean
import numpy as np # importando numpy
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
from scipy import stats # importando scipy.stats

apuesta_minima_ruleta = 1000
rojo = "Rojo"
negro = "Negro"
jugadas = []
numerosRojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]


# Definir apuesta por columna y por docena, ademas hacer que se pueda apostar por muchos a la vez
# Modificar la opcion 1 para que sea solo numero, y que se pueden apostar a varias opciones

menu = """###### MENU RULETA #######
1. JUGAR
2. SALIR
Elige: """

def solicitarDineroRuleta(saldoGlobal):
    dinero_apostado = 0
    if  saldoGlobal >= apuesta_minima_ruleta:
        dinero_apostado = float(input(f"¿Cuanto apostás a la martin gala? Debe ser al menos '{apuesta_minima_ruleta}' pesos, y no debe superar el saldo: "))
        band = True
        while band:
            if(dinero_apostado >= apuesta_minima_ruleta and dinero_apostado <= saldoGlobal):
                band = False
            else:
                dinero_apostado = float(input(f"Valor no valido, ingresa una apuesta valida: "))
    else:
        print("Tu saldo no llega al minimo para apostar.")
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

def validaSaldo(saldo):
    band = False
    if saldo < apuesta_minima_ruleta:
        print(f"Necesitas de al menos {apuesta_minima_ruleta} pesos para jugar.")
        band = True
    return band

def main():
    saldo_global = 50000 #El saldo con el que se inicia
    eleccion = ""
    while eleccion != "2":
        eleccion = input(menu)
        for i in range(3):
            print(f"Dinero disponible de su cuenta: {saldo_global}")
            if(validaSaldo(saldo_global)):
                continue
            matrizApuestas = []
            contadorMG = 0
            if(validaSaldo(saldo_global)):
                break
            dinero_apostado = solicitarDineroRuleta(saldo_global)
            if (dinero_apostado == 0):
                break
            color_eleccion_usuario = input("\t1.Rojo\n\t2.Negro\n\tElige: ")         #Para UN SOLO color
            if color_eleccion_usuario == "1":
                matrizApuestas.append([rojo, dinero_apostado])
            elif color_eleccion_usuario == "2":
                matrizApuestas.append([negro, dinero_apostado])
            else:
                print("Ingresó otra opción.")
                break
#Opcion 10 girar
        matrizInd = matrizApuestas[contadorMG]
        while (matrizInd[1] <= saldo_global):
            nRandom = ran.randint (0,36)
            saldo_global -= matrizInd[1] # le descuento al salgoGlobal lo apostado
            if(nRandom in numerosRojos and matrizInd[0] == rojo) or (nRandom not in numerosRojos and matrizInd[0] == negro):
                saldo_global += matrizInd[1]*2
                matrizApuestas.append([matrizInd[0], dinero_apostado])
                print(matrizInd, " Ganaste, el saldo global es: ", saldo_global)    
            else:
                matrizApuestas.append([matrizInd[0], matrizInd[1]*2])
                print(matrizInd, " Perdiste, el saldo global es: ", saldo_global) 
            contadorMG += 1
            matrizInd = matrizApuestas[contadorMG]
        print("Te quedaste sin saldo pa")
        print(f"Saldo final: {saldo_global}") 
    print(f"Saldo final: {saldo_global}") 
main()
