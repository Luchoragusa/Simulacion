import random
from cmath import sqrt
from xmlrpc.client import Boolean
import numpy as np # importando numpy
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
from scipy import stats # importando scipy.stats

apuesta_minima_ruleta = 10000
dinero_ganado_paridad = 15000
rojo = "Rojo"
negro = "Negro"
par = "Par"
impar = "Impar"

Ruleta = [[1,4,7,10,13,16,19,22,25,28,31,34]
         ,[2,5,8,11,14,17,20,23,26,29,32,35]
         ,[3,5,9,12,15,18,21,24,27,30,33,36]]


menu = """###### MENU RULETA #######
1. JUGAR
2. SALIR
Elige: """

explicacion_ruleta = f"""Se puede apostar por:
1) Numero y color: si acertás ambos, la apuesta se multiplica por 10. Si no, se pierde la apuesta
2) Solamente color: si se acierta el color, la apuesta se multiplica por 2. Si no, se pierde la apuesta
3) Solo paridad: si se acierta par o impar, se ganan 15000. Si no, se pierde la apuesta.
Los numeros van del 0 al 36, colores son rojo y negro, paridades son par e impar"""

#Está sin implementar, simplemente lo traje para utilizar después y no olvidarnos
conjuntoValores = []
conjuntoValoresHi = []


def solicitarDineroRuleta(saldo):
    dinero_apostado = 0
    while dinero_apostado < apuesta_minima_ruleta or dinero_apostado > saldo:
        dinero_apostado = float(input(f"¿Cuanto apostás? Debe ser al menos {apuesta_minima_ruleta} pesos, y no debe superar el saldo: "))
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
        if eleccion == "1":
            print(f"Dinero disponible: {saldo_global}")
            colores = [rojo, negro]
            if(validaSaldo(saldo_global)):
                continue

            print(explicacion_ruleta)
            dinero_apostado = solicitarDineroRuleta(saldo_global)
            eleccion_ruleta = ""
            while eleccion_ruleta != "4":
                print(f"Dinero disponible: {saldo_global}")
                eleccion_ruleta = input(""" 1. Número y color
                                            2. Solo color (negro y rojo)
                                            3. Paridad (par e impar)
                                            4. Volver
                                            Elige: """)
#Opcion 1 (Número y color)
                if eleccion_ruleta == "1":
                    
                    if(validaSaldo(saldo_global)):
                        break
                    
                    numero_usuario = pedirNumero()
                    color_eleccion_usuario = input("1. Rojo\n2.Negro\nElige: ")
                    if color_eleccion_usuario == "1":
                        color_usuario = rojo
                    else:
                        color_usuario  = negro
                    
                    #Se elige aleatoriamente
                    nRandom = random.randint(0, 36)
                    print("Numero obtenido: " + str(nRandom))
                    cRandom = colores[random.randinit(0, len(colores)-1)]
                    print("Color obtenido: " + str(cRandom))

                    if nRandom == numero_usuario and cRandom == color_eleccion_usuario:
                        #Acierta numero y color
                        print("Gana el dinero apostado multiplicado por 10.")
                        saldo_global += dinero_apostado*9
                    else:                                                                               # ver esto, pq no es asi q si no pega los 2 pierde todo
                        print("Pierde lo apostado numero y color...")
                        saldo_global -= dinero_apostado
                    pass

#Opcion 2 (Solo color)
                elif eleccion_ruleta == "2":

                    if(validaSaldo(saldo_global)):
                        break

                    color_eleccion_usuario = input("1.Rojo\n2.Negro\nElige: ")

                    if color_eleccion_usuario == "1":
                        color_usuario = rojo
                    else: 
                        color_usuario = negro

                    cRandom = colores[random.randinit(0, len(colores)-1)]
                    print("Color obtenido: " + str(cRandom))
                    if color_usuario == cRandom:
                        #Acierta color
                        print("La apuesta se multiplica por 2")
                        saldo_global += dinero_apostado * 2
                    else:
                        print("Pierde lo apostado en color...")
                        saldo_global -= dinero_apostado
                        
#Opcion 3 (paridad)
                elif eleccion_ruleta == "3":

                    if(validaSaldo(saldo_global)):
                        break

                    paridad_eleccion_usuario = input("1.Par\n2.Impar\nElige: ")

                    if paridad_eleccion_usuario == "1":
                        paridad_usuario = par
                    else:
                        paridad_usuario = impar

                    nRandom = random.randint(0, 36)
                    print("Numero obtenido: " + str(nRandom))

                    if nRandom % 2 == 0 and paridad_usuario == par:
                        print("El numero es par.")
                        print(f"Gana {dinero_ganado_paridad} pesos.")
                        saldo_global += dinero_ganado_paridad

                    elif nRandom % 2 != 0 and paridad_usuario == impar:
                        print("El numero es impar.")
                        print(f"Gana {dinero_ganado_paridad} pesos.")
                        saldo_global += dinero_ganado_paridad

                    else:
                        print("Pierde lo apostado en paridad...")
                        saldo_global -= dinero_apostado

    print(f"Saldo final: {saldo_global}")
                        
main()
