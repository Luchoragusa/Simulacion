import random as ran
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

numerosRojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Definir apuesta por columna y por docena, ademas hacer que se pueda apostar por muchos a la vez
# Modificar la opcion 1 para que sea solo numero, y que se pueden apostar a varias opciones

explicacion_ruleta = f"""\nSe puede apostar por:
1) Numero y color: si acertás ambos, la apuesta se multiplica por 10. Si no, se pierde la apuesta
2) Solamente color: si se acierta el color, la apuesta se multiplica por 2. Si no, se pierde la apuesta
3) Solo paridad: si se acierta par o impar, se ganan 15000. Si no, se pierde la apuesta.
Los numeros van del 0 al 36, colores son rojo y negro, paridades son par e impar\n"""


def solicitarDineroRuleta(saldoGlobal, apuestaActual):
    dinero_apostado = 0
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
    return dinero_apostado, apuestaActual

def pedirNumero():
    numero = int(input("Elige un numero entre 0 y 36: "))
    band = True
    while (band): 
        if 0 <= numero <= 36:
            band = False
            return numero
        else:
            band = True
            numero = int(input("Elige un numero entre 0 y 36: "))

def fibonacci(n):   #formula fibonacci aplicada a python
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def estrategiaFibonacci_Agota_Saldo(saldo):
    enesimo = 1
    mesa = ["Rojo"] * 18 + ["Negro"] * 18 + ["Verde"] * 1
    saldo_historial = []
    apuesta_historial = []
    valores_apuestas_historial = [0,0,0,0,0,0]
    apuesta_inicial = 10
    nro_tirada = []
    i=0      
    nro_tirada.append(i)
    saldo_historial.append(saldo)    
    apuesta_historial.append(apuesta_inicial) 
    while saldo > 0:
        apuesta = fibonacci(enesimo) * apuesta_inicial     #Apuesto 10 dinero al "n" que me trae       
        if apuesta > saldo:
            apuesta = saldo 
        apuesta_historial.append(apuesta)
        tirada = ran.choice(mesa)
        if apuesta==10:
            valores_apuestas_historial[0]+=1
        elif apuesta==20:
            valores_apuestas_historial[1]+=1        
        elif apuesta==30:
            valores_apuestas_historial[2]+=1
        elif apuesta==50:
            valores_apuestas_historial[3]+=1        
        elif apuesta==80:
            valores_apuestas_historial[4]+=1
        if tirada == "Rojo":
            saldo += apuesta
            enesimo = max(enesimo - 2, 1)   #traigo el max numero entre n-2 y 1
        else:
            saldo -= apuesta
            enesimo += 1
        i+=1    
        saldo_historial.append(saldo)        
        nro_tirada.append(i)
    return nro_tirada, saldo_historial, apuesta_historial, valores_apuestas_historial

def estrategiaParoli_Agota_Saldo(saldo):
    mesa = ["Rojo"] * 18 + ["Negro"] * 18 + ["Verde"] * 1
    saldo_historial = []  
    apuestas_historial = []
    valores_apuestas_historial = [0,0,0]
    nro_tirada = []
    apuesta_inicial=10
    apuesta = apuesta_inicial
    vez_apostada=1      
    i=0      
    nro_tirada.append(i)
    saldo_historial.append(saldo)
    apuestas_historial.append(apuesta_inicial)                               
    while saldo > 0:                   
        tirada = ran.choice(mesa)
        if apuesta > saldo:
            apuesta = saldo

        apuestas_historial.append(apuesta)

        if apuesta==10:
            valores_apuestas_historial[0]+=1
        elif apuesta==20:
            valores_apuestas_historial[1]+=1        
        elif apuesta==40:
            valores_apuestas_historial[2]+=1

        if tirada == "Negro":
            saldo += apuesta
            if vez_apostada==1 or vez_apostada==2:
                apuesta=apuesta*2
                vez_apostada+=1
            else:
                apuesta=apuesta_inicial
                vez_apostada=1
        else:           
            saldo -= apuesta
            apuesta=apuesta_inicial            
            vez_apostada=1
        saldo_historial.append(saldo)
        i+=1
        nro_tirada.append(i)
    return nro_tirada,saldo_historial,apuestas_historial,valores_apuestas_historial     

def estrategiaFibonacci_Tiradas(saldo,cant_tiradas):
    enesimo = 1
    mesa = ["Rojo"] * 18 + ["Negro"] * 18 + ["Verde"] * 1
    saldo_historial = []  
    apuesta_historial = []
    valores_apuestas_historial = [0,0,0,0,0]
    apuesta_inicial = 10
    apuesta_historial.append(apuesta_inicial)   
    nro_tirada = []
    saldo_historial.append(saldo)
    nro_tirada.append(0)                                      
    for i in range(cant_tiradas):      
        apuesta = fibonacci(enesimo) * apuesta_inicial      #Apuesto 0.01 dinero al "n" que me trae          
        if saldo-apuesta < 0:
            break  
        apuesta_historial.append(apuesta)
        tirada = ran.choice(mesa)
        if apuesta==10:
            valores_apuestas_historial[0]+=1
        elif apuesta==20:
            valores_apuestas_historial[1]+=1        
        elif apuesta==30:
            valores_apuestas_historial[2]+=1
        elif apuesta==50:
            valores_apuestas_historial[3]+=1        
        elif apuesta==80:
            valores_apuestas_historial[4]+=1
        if tirada == "Rojo":
            saldo += apuesta
            enesimo = max(enesimo - 2, 1)   #traigo el max numero entre n-2 y 1
        else:
            saldo -= apuesta
            enesimo += 1
        saldo_historial.append(saldo)
        nro_tirada.append(i+1)
    return nro_tirada,saldo_historial,apuesta_historial, valores_apuestas_historial

def estrategiaParoli_Tiradas(saldo,cant_tiradas):
    mesa = ["Rojo"] * 18 + ["Negro"] * 18 + ["Verde"] * 1
    saldo_historial = []  
    apuestas_historial = []
    valores_apuestas_historial = [0,0,0]
    nro_tirada = []
    apuesta_inicial=10
    apuesta=apuesta_inicial
    vez_apostada=1    
    saldo_historial.append(saldo)
    nro_tirada.append(0)
    apuestas_historial.append(apuesta_inicial)                                      
    for i in range(cant_tiradas):            
        if saldo-apuesta < 0:
            break
        tirada = ran.choice(mesa)
        apuestas_historial.append(apuesta)
        if apuesta==10:
            valores_apuestas_historial[0]+=1
        elif apuesta==20:
            valores_apuestas_historial[1]+=1        
        elif apuesta==40:
            valores_apuestas_historial[2]+=1

        if tirada == "Negro":
            saldo += apuesta
            if vez_apostada==1 or vez_apostada==2:
                apuesta=apuesta*2
                vez_apostada+=1
            else:
                apuesta=apuesta_inicial
                vez_apostada=1
        else:
            saldo -= apuesta
            apuesta=apuesta_inicial
            vez_apostada=1
        saldo_historial.append(saldo)
        nro_tirada.append(i+1)
    return nro_tirada,saldo_historial,apuestas_historial,valores_apuestas_historial    

def main():
    saldo_global = 50000 #El saldo con el que se inicia
    print(f"\nDinero disponible de su cuenta: {saldo_global}")
    saldos_globales = []
    saldos_globales.append(int(saldo_global))
    matrizApuestas = []           
    apuestaActual = 0
    print(explicacion_ruleta)
    eleccion_ruleta = ""
    eleccion_estrategia = ""
    while eleccion_estrategia != "5":
        eleccion_estrategia = input("""\n\t1. Jugar sin estrategia\n\t2. Estrategia Fibonacci\n\t3. Estrategia Martingala\n\t4. Estrategia Paroli\n\t5. Volver\n\tElige: """)
        if eleccion_estrategia == "1":
            while eleccion_ruleta != "8":
                print(f"\nDinero disponible para esta ronda: {saldo_global-apuestaActual}")
                eleccion_ruleta = input("""\n\t1. Número\n\t2. Color\n\t3. Paridad (par e impar)\n\t4. 12's\n\t5. 1-18 y/o 19-36\n\t6. 2 to 1\n\t7. Girar la ruleta\n\t8. Volver\n\tElige: """)
#Opcion 1 (Número)
                if eleccion_ruleta == "1" and (saldo_global-apuestaActual) >= apuesta_minima_ruleta:
                    dinero_apostado, apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)                       
                    numero_usuario = pedirNumero()
                    matrizApuestas.append([numero_usuario, dinero_apostado])
                elif eleccion_ruleta == "1" and (saldo_global-apuestaActual) < apuesta_minima_ruleta:
                    print("Tu saldo no llega al minimo para apostar. Se tirara la ruleta.")
                    eleccion_ruleta="7"
#Opcion 2 (Color)
                elif eleccion_ruleta == "2" and (saldo_global-apuestaActual) >= apuesta_minima_ruleta:
                    dinero_apostado, apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)                        
                    color_eleccion_usuario = input("\n\t1.Rojo\n\t2.Negro\n\tElige: ")         #Para UN SOLO color
                    while color_eleccion_usuario not in("1","2"):
                        color_eleccion_usuario = input("\nOpcion incorrecta. Ingrese 1 o 2: ")
                    if color_eleccion_usuario == "1":
                        matrizApuestas.append([rojo, dinero_apostado])
                    elif color_eleccion_usuario == "2":
                        matrizApuestas.append([negro, dinero_apostado])
                elif eleccion_ruleta == "2" and (saldo_global-apuestaActual) < apuesta_minima_ruleta:
                    print("Tu saldo no llega al minimo para apostar. Se tirara la ruleta.")
                    eleccion_ruleta="7"
                    
#Opcion 3 (paridad)
                elif eleccion_ruleta == "3" and (saldo_global-apuestaActual) >= apuesta_minima_ruleta:
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)                           
                    paridad_eleccion_usuario = input("\n\t1.Par\n\t2.Impar\n\tElige: ")       #Para UNA SOLA paridad
                    while paridad_eleccion_usuario not in("1","2"):
                        paridad_eleccion_usuario= input("\nOpcion incorrecta. Ingrese 1 o 2: ")
                    if paridad_eleccion_usuario == "1":
                        matrizApuestas.append([par, dinero_apostado])
                    elif paridad_eleccion_usuario == "2":
                        matrizApuestas.append([impar, dinero_apostado])    
                elif eleccion_ruleta == "3" and (saldo_global-apuestaActual) < apuesta_minima_ruleta:
                    print("Tu saldo no llega al minimo para apostar. Se tirara la ruleta.")
                    eleccion_ruleta="7"                       
#Opcion 4 12's
                elif eleccion_ruleta == "4" and (saldo_global-apuestaActual) >= apuesta_minima_ruleta:
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)                         
                    docena_eleccion_usuario = input("\n\t1.1ra docena\n\t2.2da docena\n\t3.3ra docena\n\tElige: ")   #Para UNA SOLA docena
                    while docena_eleccion_usuario not in("1","2","3"):
                        docena_eleccion_usuario= input("\nOpcion incorrecta. Ingrese 1 o 2 o 3: ")
                    if docena_eleccion_usuario == "1":
                        matrizApuestas.append([docena1, dinero_apostado])
                    elif docena_eleccion_usuario == "2":
                        matrizApuestas.append([docena2, dinero_apostado])
                    elif docena_eleccion_usuario == "3":
                        matrizApuestas.append([docena3, dinero_apostado])  
                elif eleccion_ruleta == "4" and (saldo_global-apuestaActual) < apuesta_minima_ruleta:
                    print("Tu saldo no llega al minimo para apostar. Se tirara la ruleta.")
                    eleccion_ruleta="7"                          
#Opcion 5 1-18 o 19-36
                elif eleccion_ruleta == "5" and (saldo_global-apuestaActual) >= apuesta_minima_ruleta:
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)                         
                    faltapasa_eleccion_usuario = input("\n\t1.1-18\n\t2.19-36\n\tElige: ")   #Para UNA SOLA 
                    while faltapasa_eleccion_usuario not in("1","2"):
                        faltapasa_eleccion_usuario= input("\nOpcion incorrecta. Ingrese 1 o 2: ")
                    if faltapasa_eleccion_usuario == "1":
                        matrizApuestas.append([falta, dinero_apostado])
                    elif faltapasa_eleccion_usuario == "2":
                        matrizApuestas.append([pasa, dinero_apostado])
                elif eleccion_ruleta == "5" and (saldo_global-apuestaActual) < apuesta_minima_ruleta:
                    print("Tu saldo no llega al minimo para apostar. Se tirara la ruleta.")
                    eleccion_ruleta="7"
#Opcion 6 columnas
                elif eleccion_ruleta == "6" and (saldo_global-apuestaActual) >= apuesta_minima_ruleta:
                    dinero_apostado,apuestaActual = solicitarDineroRuleta(saldo_global, apuestaActual)                        
                    columna_eleccion_usuario = input("\n\t1.1ra columna\n\t2.2da columna\n\t3.3ra columna\n\tElige: ")   #Para UNA SOLA docena
                    while columna_eleccion_usuario not in("1","2","3"):
                        columna_eleccion_usuario= input("\nOpcion incorrecta. Ingrese 1 o 2 o 3: ")
                    if columna_eleccion_usuario == "1":
                        matrizApuestas.append([columna1, dinero_apostado])
                    elif columna_eleccion_usuario == "2":
                        matrizApuestas.append([columna2, dinero_apostado])
                    elif columna_eleccion_usuario == "3":
                        matrizApuestas.append([columna3, dinero_apostado]) 
                elif eleccion_ruleta == "6" and (saldo_global-apuestaActual) < apuesta_minima_ruleta:
                    print("Tu saldo no llega al minimo para apostar. Se tirara la ruleta.")
                    eleccion_ruleta="7"                       
#Opcion 7 Girar ruleta 
                if eleccion_ruleta == "7": #genero el numero y analizo cada condicion
                    nRandom = ran.randint (0,36)
                    numerosRandom = []
                    numerosRandom.append(nRandom)
                    print("Salio el: ", nRandom)
                    saldo_global -= apuestaActual # le descuento al salgoGlobal lo apostado
                    ganancia = 0
                    for i in range(int(np.size(matrizApuestas)/2)):
                        m = matrizApuestas[i]
                        # Si acierto el Numero
                        if(m[0] == nRandom): 
                            ganancia += m[1]*36
                        # Si acierto el Color
                        if(nRandom in numerosRojos and m[0] == rojo) or (nRandom not in numerosRojos and m[0] == negro):
                                ganancia += m[1]*2
                        # Si acierto la paridad
                        if (nRandom %2 == 0 and m[0] == par) or (nRandom % 2 != 0 and m[0] == impar):
                            ganancia += m[1] * 2
                        # Si acierto los 12's
                        if (nRandom >= 1 and nRandom <= 12 and m[0] == docena1) or (nRandom >= 13 and nRandom <= 24 and m[0] == docena2) or (nRandom >= 25 and nRandom <= 36 and m[0] == docena3):
                            ganancia += m[1] * 3
                        # Si acerto los 1-18 o 19-36
                        if (nRandom >= 1 and nRandom <= 18 and m[0] == falta) or (nRandom >= 19 and nRandom <= 36 and m[0] == pasa):
                            ganancia += m[1] * 2
                        # Si acerto la columna
                        if (nRandom in columna1 and m[0] == columna1) or (nRandom in columna2 and m[0] == columna2) or (nRandom in columna3 and m[0] == columna3):
                            ganancia += m[1] * 3
                        #??????    Si acierto la Martingala color
                        #??????    ganancia += m[1] * 2 # Nose si se multiplica por 2
                    saldo_global += ganancia # Sumo la ganancia q haya tenido el usuario
                    saldos_globales.append(int(saldo_global))
                    apuestaActual=0
                    matrizApuestas.clear()
            print(f"\nSaldo final: {saldo_global}") 
            nro_rondas = []
            for i in range(np.size(saldos_globales)):
                nro_rondas.append(int(i))
            plt.plot(nro_rondas,saldos_globales)
            plt.xlabel("Numero de rondas")
            plt.ylabel("Saldo")
            plt.title("Evolución de saldo sin estrategia")
            plt.axhline(y=50000, color = "r")
            plt.show()

#Opcion 8 ESTRATEGIA Fibonacci
        elif eleccion_estrategia == "2":
            eleccion_modo_fibo = input("\t¿Como desea jugar? \n\t1. Jugar hasta agotar saldo\n\t2. Jugar 25, 50 y 75 tiradas\n\tElige: ")
            if eleccion_modo_fibo=="1":                        
                saldo_eleccion_fibo = 100     
                plt.figure(2)
                fig2,axs2=plt.subplots(2, 2)
                plt.figure(3)
                fig,axs=plt.subplots(2, 2)               
                for i in range(5):  
                    arreglo_x=[]
                    arreglo_y=[]
                    apuestasHistorial=[]
                    valoresApuestasHistorial=[]
                    arreglo_x,arreglo_y,apuestasHistorial,valoresApuestasHistorial=estrategiaFibonacci_Agota_Saldo(saldo_eleccion_fibo)
                    plt.figure(1) 
                    plt.plot(arreglo_x,arreglo_y)                   
                    plt.figure(2)
                    if i==0:
                        axs2[0,0].plot(arreglo_x,apuestasHistorial,marker='o')
                        axs2[0,0].set_title("Corrida "+str(i+1))
                        axs2[0,0].set(ylabel='Apuestas')
                    elif i==1:
                        axs2[0,1].plot(arreglo_x,apuestasHistorial, 'tab:orange',marker='o')
                        axs2[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs2[1,0].plot(arreglo_x,apuestasHistorial, 'tab:green',marker='o')  
                        axs2[1,0].set_title("Corrida "+str(i+1))
                        axs2[1,0].set(xlabel='Numero de Tiradas', ylabel='Apuestas')
                    elif i==3:
                        axs2[1,1].plot(arreglo_x,apuestasHistorial, 'tab:red',marker='o')
                        axs2[1,1].set_title("Corrida "+str(i+1))
                        axs2[1,1].set(xlabel='Numero de Tiradas')
                    plt.figure(3)
                    total_valores_apuestas=valoresApuestasHistorial[0]+valoresApuestasHistorial[1]+valoresApuestasHistorial[2]+valoresApuestasHistorial[3]+valoresApuestasHistorial[4]
                    frecuenciasValoresApuestasHistorial=[0,0,0,0,0]
                    frecuenciasValoresApuestasHistorial[0]=valoresApuestasHistorial[0]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[1]=valoresApuestasHistorial[1]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[2]=valoresApuestasHistorial[2]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[3]=valoresApuestasHistorial[3]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[4]=valoresApuestasHistorial[4]/total_valores_apuestas
                    eje_x_barras=["10","20","30","50","80"]
                    if i==0:
                        axs[0,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial, width= 0.25)
                        axs[0,0].set_title("Corrida "+str(i+1))
                        axs[0,0].set(ylabel='Frecuencia relativa')
                    elif i==1:
                        axs[0,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="orange", width= 0.25)
                        axs[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs[1,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="green", width= 0.25)
                        axs[1,0].set_title("Corrida "+str(i+1))
                        axs[1,0].set(xlabel='Valor apostado', ylabel='Frecuencia relativa')
                    elif i==3:
                        axs[1,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="red", width= 0.25)
                        axs[1,1].set_title("Corrida "+str(i+1))
                        axs[1,1].set(xlabel='Valor apostado')
                plt.figure(1)
                plt.xlabel("Numero de Tiradas")
                plt.ylabel("Saldo")
                texto_titulo=f"Evolución del saldo partiendo de ${str(saldo_eleccion_fibo)} hasta agotarlo en 4 corridas"
                plt.title(texto_titulo)
                plt.axhline(y=saldo_eleccion_fibo, color = "r")               
                plt.figure(2)
                texto_titulo=f"Evolución de las apuestas partiendo de ${str(saldo_eleccion_fibo)} de 4 corridas"
                fig2.suptitle(texto_titulo)    
                plt.figure(3)
                texto_titulo=f"Frecuencia relativa de los valores de las apuestas de las 4 corridas"
                fig.suptitle(texto_titulo)                              
                plt.show()
            elif(eleccion_modo_fibo=="2"):             
                saldo_eleccion_fibo = 100 
                cant_tiradas_fibo = int(input("\nElija cuantas tiradas realiza (25,50 o 75): ")) 
                while cant_tiradas_fibo not in (25,50,75):
                    cant_tiradas_fibo = int(input("\nMAL!! Elija cuantas tiradas realiza (25,50 o 75): "))                                    
                plt.figure(2)
                fig2,axs2=plt.subplots(2, 2)
                plt.figure(3)
                fig,axs=plt.subplots(2, 2)
                for i in range(4):
                    arreglo_x=[]
                    arreglo_y=[]
                    apuestasHistorial=[]
                    valoresApuestasHistorial=[]
                    arreglo_x,arreglo_y,apuestasHistorial,valoresApuestasHistorial=estrategiaFibonacci_Tiradas(saldo_eleccion_fibo,cant_tiradas_fibo)
                    plt.figure(1)                
                    plt.plot(arreglo_x,arreglo_y)               
                    plt.figure(2)
                    if i==0:
                        axs2[0,0].plot(arreglo_x,apuestasHistorial,marker='o')
                        axs2[0,0].set_title("Corrida "+str(i+1))
                        axs2[0,0].set(ylabel='Apuestas')
                    elif i==1:
                        axs2[0,1].plot(arreglo_x,apuestasHistorial, 'tab:orange',marker='o')
                        axs2[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs2[1,0].plot(arreglo_x,apuestasHistorial, 'tab:green',marker='o')  
                        axs2[1,0].set_title("Corrida "+str(i+1))
                        axs2[1,0].set(xlabel='Numero de Tiradas', ylabel='Apuestas')
                    elif i==3:
                        axs2[1,1].plot(arreglo_x,apuestasHistorial, 'tab:red',marker='o')
                        axs2[1,1].set_title("Corrida "+str(i+1))
                        axs2[1,1].set(xlabel='Numero de Tiradas')
                    plt.figure(3)
                    total_valores_apuestas=valoresApuestasHistorial[0]+valoresApuestasHistorial[1]+valoresApuestasHistorial[2]+valoresApuestasHistorial[3]+valoresApuestasHistorial[4]
                    frecuenciasValoresApuestasHistorial=[0,0,0,0,0]
                    frecuenciasValoresApuestasHistorial[0]=valoresApuestasHistorial[0]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[1]=valoresApuestasHistorial[1]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[2]=valoresApuestasHistorial[2]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[3]=valoresApuestasHistorial[3]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[4]=valoresApuestasHistorial[4]/total_valores_apuestas
                    eje_x_barras=["10","20","30","50","80"]
                    if i==0:
                        axs[0,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial, width= 0.25)
                        axs[0,0].set_title("Corrida "+str(i+1))
                        axs[0,0].set(ylabel='Frecuencia relativa')
                    elif i==1:
                        axs[0,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="orange", width= 0.25)
                        axs[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs[1,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="green", width= 0.25)
                        axs[1,0].set_title("Corrida "+str(i+1))
                        axs[1,0].set(xlabel='Valor apostado', ylabel='Frecuencia relativa')
                    elif i==3:
                        axs[1,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="red", width= 0.25)
                        axs[1,1].set_title("Corrida "+str(i+1))
                        axs[1,1].set(xlabel='Valor apostado')               
                plt.figure(1)
                plt.xlabel("Numero de Tiradas")
                plt.ylabel("Saldo")
                texto_titulo=f"Evolución del saldo partiendo de ${str(saldo_eleccion_fibo)} de 4 corridas en {str(cant_tiradas_fibo)} tiradas"
                plt.title(texto_titulo)
                plt.axhline(y=saldo_eleccion_fibo, color = "r")
                plt.figure(2)
                texto_titulo=f"Evolución de las apuestas partiendo de ${str(saldo_eleccion_fibo)} de 4 corridas en {str(cant_tiradas_fibo)} tiradas"
                fig2.suptitle(texto_titulo)   
                plt.figure(3)
                texto_titulo=f"Frecuencia relativa del promedio de los valores de las apuestas de las 4 corridas en {str(cant_tiradas_fibo)} tiradas"
                fig.suptitle(texto_titulo)  
                plt.show()
            else:
                print("Ingresó otra opción distinta a la solicitada.")
#Opcion 9 ESTRATEGIA Paroli
        elif eleccion_estrategia == "4":    
            eleccion_modo_paroli = input("\t¿Como desea jugar? \n\t1. Jugar hasta agotar saldo\n\t2. Jugar 25, 50 y 75 tiradas\n\tElige: ")
            if eleccion_modo_paroli=="1":
                saldo_eleccion_paroli =100 # int(input("\nElija el saldo inicial: "))                                      
                plt.figure(2)
                fig2,axs2=plt.subplots(2, 2)
                plt.figure(3)
                fig,axs=plt.subplots(2, 2)               
                for i in range(4):  
                    arreglo_x=[]
                    arreglo_y=[]
                    apuestasHistorial=[]
                    valoresApuestasHistorial=[]
                    arreglo_x,arreglo_y,apuestasHistorial,valoresApuestasHistorial=estrategiaParoli_Agota_Saldo(saldo_eleccion_paroli)
                    plt.figure(1) 
                    plt.plot(arreglo_x,arreglo_y)                   
                    plt.figure(2)
                    if i==0:
                        axs2[0,0].plot(arreglo_x,apuestasHistorial,marker='o')
                        axs2[0,0].set_title("Corrida "+str(i+1))
                        axs2[0,0].set(ylabel='Apuestas')
                    elif i==1:
                        axs2[0,1].plot(arreglo_x,apuestasHistorial, 'tab:orange',marker='o')
                        axs2[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs2[1,0].plot(arreglo_x,apuestasHistorial, 'tab:green',marker='o')  
                        axs2[1,0].set_title("Corrida "+str(i+1))
                        axs2[1,0].set(xlabel='Numero de Tiradas', ylabel='Apuestas')
                    elif i==3:
                        axs2[1,1].plot(arreglo_x,apuestasHistorial, 'tab:red',marker='o')
                        axs2[1,1].set_title("Corrida "+str(i+1))
                        axs2[1,1].set(xlabel='Numero de Tiradas')
                    plt.figure(3)
                    total_valores_apuestas=valoresApuestasHistorial[0]+valoresApuestasHistorial[1]+valoresApuestasHistorial[2]
                    frecuenciasValoresApuestasHistorial=[0,0,0]
                    frecuenciasValoresApuestasHistorial[0]=valoresApuestasHistorial[0]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[1]=valoresApuestasHistorial[1]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[2]=valoresApuestasHistorial[2]/total_valores_apuestas
                    eje_x_barras=["10","20","40"]
                    if i==0:
                        axs[0,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial, width= 0.25)
                        axs[0,0].set_title("Corrida "+str(i+1))
                        axs[0,0].set(ylabel='Frecuencia relativa')
                    elif i==1:
                        axs[0,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="orange", width= 0.25)
                        axs[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs[1,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="green", width= 0.25)
                        axs[1,0].set_title("Corrida "+str(i+1))
                        axs[1,0].set(xlabel='Valor apostado', ylabel='Frecuencia relativa')
                    elif i==3:
                        axs[1,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="red", width= 0.25)
                        axs[1,1].set_title("Corrida "+str(i+1))
                        axs[1,1].set(xlabel='Valor apostado')
                plt.figure(1)
                plt.xlabel("Numero de Tiradas")
                plt.ylabel("Saldo")
                texto_titulo=f"Evolución del saldo partiendo de ${str(saldo_eleccion_paroli)} hasta agotarlo en 4 corridas"
                plt.title(texto_titulo)
                plt.axhline(y=saldo_eleccion_paroli, color = "r")               
                plt.figure(2)
                texto_titulo=f"Evolución de las apuestas partiendo de ${str(saldo_eleccion_paroli)} de 4 corridas"
                fig2.suptitle(texto_titulo)    #Para escribir el titulo de cada grafiquito
                #for ax2 in axs2.flat:         #Para escribir los label de los ejes
                #    ax2.set(xlabel='Numero de Tiradas', ylabel='Apuestas')
                #for ax2 in fig2.get_axes():   #Para que compartan label los ejes
                #    ax2.label_outer()
                plt.figure(3)
                texto_titulo=f"Frecuencia relativa de los valores de las apuestas de las 4 corridas"
                fig.suptitle(texto_titulo)                              
                plt.show()

            elif(eleccion_modo_paroli=="2"):
                
                saldo_eleccion_paroli = 100 #int(input("\nElija el saldo inicial: "))  
                cant_tiradas_paroli = int(input("\nElija cuantas tiradas realiza (25,50 o 75): ")) 
                while cant_tiradas_paroli not in (25,50,75):
                    cant_tiradas_paroli = int(input("\nMAL!! Elija cuantas tiradas realiza (25,50 o 75): "))                     
                
                plt.figure(2)
                fig2,axs2=plt.subplots(2, 2)

                plt.figure(3)
                fig,axs=plt.subplots(2, 2)

                for i in range(4):
                    arreglo_x=[]
                    arreglo_y=[]
                    apuestasHistorial=[]
                    valoresApuestasHistorial=[]
                    arreglo_x,arreglo_y,apuestasHistorial,valoresApuestasHistorial=estrategiaParoli_Tiradas(saldo_eleccion_paroli,cant_tiradas_paroli)
                    plt.figure(1)                
                    plt.plot(arreglo_x,arreglo_y)
                    
                    plt.figure(2)
                    if i==0:
                        axs2[0,0].plot(arreglo_x,apuestasHistorial,marker='o')
                        axs2[0,0].set_title("Corrida "+str(i+1))
                        axs2[0,0].set(ylabel='Apuestas')
                    elif i==1:
                        axs2[0,1].plot(arreglo_x,apuestasHistorial, 'tab:orange',marker='o')
                        axs2[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs2[1,0].plot(arreglo_x,apuestasHistorial, 'tab:green',marker='o')  
                        axs2[1,0].set_title("Corrida "+str(i+1))
                        axs2[1,0].set(xlabel='Numero de Tiradas', ylabel='Apuestas')
                    elif i==3:
                        axs2[1,1].plot(arreglo_x,apuestasHistorial, 'tab:red',marker='o')
                        axs2[1,1].set_title("Corrida "+str(i+1))
                        axs2[1,1].set(xlabel='Numero de Tiradas')

                    plt.figure(3)
                    total_valores_apuestas=valoresApuestasHistorial[0]+valoresApuestasHistorial[1]+valoresApuestasHistorial[2]
                    frecuenciasValoresApuestasHistorial=[0,0,0]
                    frecuenciasValoresApuestasHistorial[0]=valoresApuestasHistorial[0]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[1]=valoresApuestasHistorial[1]/total_valores_apuestas
                    frecuenciasValoresApuestasHistorial[2]=valoresApuestasHistorial[2]/total_valores_apuestas

                    eje_x_barras=["10","20","40"]
                    if i==0:
                        axs[0,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial, width= 0.25)
                        axs[0,0].set_title("Corrida "+str(i+1))
                        axs[0,0].set(ylabel='Frecuencia relativa')
                    elif i==1:
                        axs[0,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="orange", width= 0.25)
                        axs[0,1].set_title("Corrida "+str(i+1))
                    elif i==2:
                        axs[1,0].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="green", width= 0.25)
                        axs[1,0].set_title("Corrida "+str(i+1))
                        axs[1,0].set(xlabel='Valor apostado', ylabel='Frecuencia relativa')
                    elif i==3:
                        axs[1,1].bar(eje_x_barras,frecuenciasValoresApuestasHistorial,color="red", width= 0.25)
                        axs[1,1].set_title("Corrida "+str(i+1))
                        axs[1,1].set(xlabel='Valor apostado')
                
                plt.figure(1)
                plt.xlabel("Numero de Tiradas")
                plt.ylabel("Saldo")
                texto_titulo=f"Evolución del saldo partiendo de ${str(saldo_eleccion_paroli)} de 4 corridas en {str(cant_tiradas_paroli)} tiradas"
                plt.title(texto_titulo)
                plt.axhline(y=saldo_eleccion_paroli, color = "r")

                plt.figure(2)
                texto_titulo=f"Evolución de las apuestas partiendo de ${str(saldo_eleccion_paroli)} de 4 corridas en {str(cant_tiradas_paroli)} tiradas"
                fig2.suptitle(texto_titulo)    #Para escribir el titulo de cada grafiquito
                #for ax2 in axs2.flat:         #Para escribir los label de los ejes
                #    ax2.set(xlabel='Numero de Tiradas', ylabel='Apuestas')
                #for ax2 in fig2.get_axes():   #Para que compartan label los ejes
                #    ax2.label_outer()

                plt.figure(3)
                texto_titulo=f"Frecuencia relativa del promedio de los valores de las apuestas de las 4 corridas en {str(cant_tiradas_paroli)} tiradas"
                fig.suptitle(texto_titulo)  

                plt.show()
            else:
                print("Ingresó otra opción distinta a la solicitada.")
main()