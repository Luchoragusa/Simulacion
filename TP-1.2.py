import random
from cmath import sqrt
from xmlrpc.client import Boolean
import numpy as np # importando numpy
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
from scipy import stats # importando scipy.stats

numeroRandomObtenido = 0
apuesta_minima_ruleta = 10000
dinero_ganado_paridad = 15000
rojo = "Rojo"
negro = "Negro"
par = "Par"
impar = "Impar"
docena1 = "1ra docena"
docena2 = "2da docena"
docena3 = "3ra docena"
falta = "1-18"
pasa = "19-36"
columna1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
columna2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
columna3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

matrizR = [[1,4,7,10,13,16,19,22,25,28,31,34]
        ,[2,5,8,11,14,17,20,23,26,29,32,35]
        ,[3,5,9,12,15,18,21,24,27,30,33,36]]

# Definir apuesta por columna y por docena, ademas hacer que se pueda apostar por muchos a la vez
# Modificar la opcion 1 para que sea solo numero, y que se pueden apostar a varias opciones

menu = """###### MENU RULETA #######
1. JUGAR
2. SALIR
Elige: """

explicacion_ruleta = f"""\nSe puede apostar por:
1) Numero y color: si acertás ambos, la apuesta se multiplica por 10. Si no, se pierde la apuesta
2) Solamente color: si se acierta el color, la apuesta se multiplica por 2. Si no, se pierde la apuesta
3) Solo paridad: si se acierta par o impar, se ganan 15000. Si no, se pierde la apuesta.
Los numeros van del 0 al 36, colores son rojo y negro, paridades son par e impar\n"""

colores = [rojo, negro]
docenas = [docena1, docena2, docena3]
faltapasa = [falta, pasa]
columnas = [columna1, columna2, columna3]

color_usuario = ""


def solicitarDineroRuleta(saldoGlobal, apuestaActual):
    dinero_apostado = 0
    if  (saldoGlobal-apuestaActual) >= apuesta_minima_ruleta:
        print(f"Tu saldo actual es: {saldoGlobal-apuestaActual}")
        dinero_apostado = float(input(f"¿Cuanto apostás? Debe ser al menos '{apuesta_minima_ruleta}' pesos, y no debe superar el saldo: "))
        band = True
        while band:
            if(dinero_apostado >= apuesta_minima_ruleta):
                if ((saldoGlobal-(apuestaActual + dinero_apostado)) >= 0):
                    apuestaActual += dinero_apostado
                    band = False
                else:
                    dinero_apostado = float(input(f"Te pasaste de la apuesta maxima que podes hacer, la cual es '{(saldoGlobal-apuestaActual)}' pesos: "))
            else: 
                dinero_apostado = float(input(f"Estas apostando menos de lo sugerida, ingresa una valor >= a 10000: "))
    else:
        print("Tu saldo no llega al minimo para apostar.")
    return dinero_apostado, apuestaActual

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

def girarLaRuleta():
    numeroRandomObtenido = random.randint(0, 36)
    return numeroRandomObtenido

def main():
    saldo_global = 50000 #El saldo con el que se inicia
    eleccion = ""
    while eleccion != "2":
        eleccion = input(menu)
        if eleccion == "1":
            print(f"Dinero disponible de su cuenta: {saldo_global}")
            if(validaSaldo(saldo_global)):
                continue
            matrizApuestas = []
            apuestaActual = 0
            print(explicacion_ruleta)
            eleccion_ruleta = ""
            while eleccion_ruleta != "8":
                print(f"Dinero disponible para esta ronda: {saldo_global-apuestaActual}")
                eleccion_ruleta = input("""\t1. Número\n\t2. Color\n\t3. Paridad (par e impar)\n\t4. 12's\n\t5. 1-18 y/o 19-36\n\t6. 2 to 1\n\t7. Girar la ruleta\n\t8. Volver\n\tElige: """)
#Opcion 1 (Número)
                if eleccion_ruleta == "1":
                    if(validaSaldo(saldo_global)):
                        break
                    dinero_apostado, apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)
                    if (dinero_apostado == 0):
                        break
                    numero_usuario = pedirNumero()
                    matrizApuestas.append([numero_usuario, dinero_apostado])

#Opcion 2 (Solo color)
                elif eleccion_ruleta == "2":
                    if(validaSaldo(saldo_global)):
                        break
                    dinero_apostado, apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)
                    color_eleccion_usuario = input("\t1.Rojo\n\t2.Negro\n\tElige: ")         #Para UN SOLO color
                    if color_eleccion_usuario == "1":
                        matrizApuestas.append([rojo, dinero_apostado])
                    elif color_eleccion_usuario == "2":
                        matrizApuestas.append([negro, dinero_apostado])
                    else:
                        print("Ingresó otra opción.")
                    print(matrizApuestas)

#Opcion 3 (paridad)
                elif eleccion_ruleta == "3":
                    if(validaSaldo(saldo_global)):
                        break
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)
                    paridad_eleccion_usuario = input("\t1.Par\n\t2.Impar\n\tElige: ")       #Para UNA SOLA paridad
                    if paridad_eleccion_usuario == "1":
                        matrizApuestas.append([par, dinero_apostado])
                    elif paridad_eleccion_usuario == "2":
                        matrizApuestas.append([impar, dinero_apostado])
                    else:
                        print("Ingresó otra opción.")
                        break
#Opcion 4 12's
                elif eleccion_ruleta == "4":
                    if(validaSaldo(saldo_global)):
                        break
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)
                    docena_eleccion_usuario = input("\t1.1ra docena\n\t2.2da docena\n\t3.3ra docena\n\tElige: ")   #Para UNA SOLA docena
                    if docena_eleccion_usuario == "1":
                        docena_usuario = docena1
                    elif docena_eleccion_usuario == "2":
                        docena_usuario = docena2
                    elif docena_eleccion_usuario == "3":
                        docena_usuario = docena3
                    else:
                        print("Ingresó otra opción.")
                        break
                    dRandom = docenas[random.randinit(0, len(docenas)-1)]
                    print("Docena obtenida: " + str(dRandom))
                    if docena_usuario == dRandom:
                        #Acierta docena
                        print("¡Acertaste la docena!.")
                        apuestaActual += dinero_apostado * 3
                    else:
                        print("El numero pertenece a otra docena. Pierde lo apostado.")
                        apuestaActual -= dinero_apostado
#Opcion 5 1-18 y/o 19-36
                elif eleccion_ruleta == "5":
                    if(validaSaldo(saldo_global)):
                        break
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)
                    faltapasa_eleccion_usuario = input("\t1.1-18\n\t2.19-36\n\tElige: ")   #Para UNA SOLA 
                    if faltapasa_eleccion_usuario == "1":
                        faltapasa_usuario = falta
                    elif faltapasa_eleccion_usuario == "2":
                        faltapasa_usuario = pasa
                    else:
                        print("Ingresó otra opción.")
                        break
                    fpRandom = faltapasa[random.randinit(0, len(faltapasa)-1)]
                    print("Docena obtenida: " + str(dRandom))
                    if faltapasa_usuario == fpRandom:
                        #Acierta 
                        print("¡Acertaste!.")
                        apuestaActual += dinero_apostado * 2
                    else:
                        print(f"Su numero elegido no pertenece a '{faltapasa_usuario}', pertenece a '{fpRandom}. Pierde lo apostado.'")
                        apuestaActual -= dinero_apostado
#Opcion 6 columnas
                elif eleccion_ruleta == "6":
                    if(validaSaldo(saldo_global)):
                        break
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)
                    columna_eleccion_usuario = input("\t1.1ra columna\n\t2.2da columna\n\t3.3ra columna\n\tElige: ")   #Para UNA SOLA docena
                    if columna_eleccion_usuario == "1":
                        columna_usuario = columna1
                    elif columna_eleccion_usuario == "2":
                        columna_usuario = columna2
                    elif columna_eleccion_usuario == "3":
                        columna_usuario = columna3
                    else:
                        print("Ingresó otra opción.")
                        break
                    print("Numero obtenida: " + str(numeroRandomObtenido))
                    if nRandom in columna_usuario:
                        #Acierta columna
                        print("¡Acertaste la columna!.")
                        apuestaActual += dinero_apostado * 3
                    else:
                        print(f"El numero '{nRandom}' pertenece a otra columna. Pierde lo apostado.")
                        apuestaActual -= dinero_apostado

            print(f"Saldo final: {saldo_global-apuestaActual}")                        
main()
