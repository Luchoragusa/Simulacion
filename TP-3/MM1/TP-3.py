import random as ran
import math
import simpy as sim
import matplotlib.pyplot as plt

# Usando Simpy: https://naps.com.mx/blog/simulacion-en-python-usando-simpy/

#===============================================================================================
#                                       MM1
#=============================================================================================== 
def mm1():
    titulo = 'Sistema de colas MM1'
    print(titulo.center(80, '='))
    for i in range(10):    
        µ = ran.randint(5,10)                          # el promedio de clientes atendidos por hora
        λ = [µ*0.25, µ*0.5, µ*0.75, µ, µ*1.25]         # el promedio de clientes por hora  
        for j in range(len(λ)):
            if µ > λ[j]:
                Ls = λ[j]/(µ-λ[j])
                Ws = 1/(µ-λ[j])
                Wsl = Ws*60
                Lq = Ls*λ[j]/µ
                Wq = Ws*λ[j]/µ
                Wql = Wq*60
                pu = λ[j]/µ
                po = 1 - pu
                pe = (1 - (λ[j]/µ)) * ((λ[j]/µ) * (λ[j]/µ))

                print(f"\n\n==============Repeticion {i+1} & Corrida lambda {j+1}================================")
                print(f'Clientes en el sistema: {round(Ls)} ')
                print(f'Tiempo en el sistema: {round(Ws)} Horas')
                print(f'Tiempo en el sistema: {Wsl} minutos')
                print(f'Clientes en cola: {round(Lq)}')
                print(f'Tiempo en la cola: {round(Wq)} horas')
                print(f'Tiempo en la cola: {round(Wql)}')
                print(f'Porcentaje servidor ocupado: {pu*100}')
                print(f'Porcentaje servidor ocioso: {po*100}')
                print(f'Probabilidad de que se encuentren 2 clientes: {pe*100}\n\n')
            else: #No va a existir una cola adecuada para nuestro sistema
                print(f"\n\n===========Repeticion {i+1} & Corrida lambda {j+1}===============\n")
                titulo2 = 'Cola infinita'
                print(titulo2.center(80, '='))
                print("")
                opcion = 'Se puede hacer calculo de sistema sin cola'
                print(opcion.center(80, '*'))

                trafico = λ[j]/µ
                Cperdidos = trafico/(trafico+1)
                print(f"Porcentaje de perdidos: {Cperdidos*100} %")

                print("Si el horario de atencion consta de 8 horas")
                totalC = µ*8
                print(f"Aproximadamente la cantidad de clientes en un dia es: {totalC}")

                peridas = totalC*Cperdidos
                print(f"Aproximadamente se perdieron: {peridas} clientes")

                atendidos = totalC-peridas
                print(f"Aproximadamente se atendieron: {atendidos} clientes")

#===============================================================================================
#                                  Linea de Espera
#===============================================================================================
'''
    Mediante el numero de clientes seteado, se puede ver por cada cliente:
        1. Su tiempo de llegada
        2. Su tiempo de espera
        3. Su tiempo de servicio
        4. Su tiempo de salida
'''
def lineaDeEspera():
    i = 0
    clientes = []
    tiempo_llegada = []
    tiempo_espera = []
    tiempo_servicios = []
    tiempo_ocio_servidor = []
    tiempo_salida_clientes = []
    clientes_en_sistema = []
    num_clientes = 50
    while(i < num_clientes):
        if(i == 0):
            clientes.append(i)
            tiempo_llegada.append(i)
            tiempo_espera.append(i)
            tiempo_servicios.append(ran.random())
            tiempo_ocio_servidor.append(i)
            tiempo_salida_clientes.append(tiempo_llegada[i] + tiempo_espera[i] + tiempo_servicios[i])
        if(i >= 1):
            clientes.append(i)
            tiempo_llegada.append(tiempo_llegada[i-1] + ran.random())
            tiempo_espera.append(max(tiempo_salida_clientes[i-1], tiempo_llegada[i]) - tiempo_llegada[i])
            tiempo_servicios.append(ran.random())
            tiempo_ocio_servidor.append(max(tiempo_salida_clientes[i-1], tiempo_llegada[i])-tiempo_salida_clientes[i-1])
            tiempo_salida_clientes.append(tiempo_llegada[i] + tiempo_espera[i] + tiempo_servicios[i])
        i = i + 1
    i = 0
    guion = '='
    for i in range(num_clientes):
        print(f"\nCliente: {round(clientes[i], 2)} || Tiempo de llegada: {round(tiempo_llegada[i],2)} || Tiempo de espera: {round(tiempo_espera[i],2)} || Tiempo de servicio: {round(tiempo_servicios[i],2)} || Tiempo de salida: {round(tiempo_salida_clientes[i],2)}")
        print(guion.center(120, '='))
        clientes_en_sistema.append(round(tiempo_salida_clientes[i],2) - round(tiempo_llegada[i],2))
        
        #plt.bar(clientes[i], round(tiempo_espera[i],2))                                # Evaluacion del tiempo de espera de cada cliente (en cola)
        #plt.bar(clientes[i], clientes_en_sistema[i])                                   # Evaluacion de clientes en el sistema
        #plt.bar(clientes[i], round(tiempo_ocio_servidor[i],2))                         # Evaluacion del tiempo de ocio del servidor
        #plt.bar(clientes[i], round(tiempo_salida_clientes[i],2))                       # Evaluacion del tiempo de salida de cada cliente
        #plt.bar(clientes[i], round(tiempo_llegada[i],2))                               # Evaluacion del tiempo de llegada de cada cliente
        #plt.bar(clientes[i], round(tiempo_servicios[i],2))                             # Evaluacion del tiempo de servicio de cada cliente
        #plt.bar(round(tiempo_servicios[i], 2), round(tiempo_salida_clientes[i],2))     # Evaluacion de la duracion del servicio hasta la salida del cliente
    
    plt.xlabel("Numero de repeticiones")
    plt.ylabel("Resultados")
    #plt.title("Evaluacion del tiempo de espera de cada cliente")
    #plt.title("Evaluacion de clientes en el sistema")
    #plt.title("Evaluacion del tiempo de ocio del servidor")
    #plt.title("Evaluacion del tiempo de salida de cada cliente")
    #plt.title("Evaluacion del tiempo de llegada de cada cliente")
    #plt.title("Evaluacion del tiempo de servicio de cada cliente")
    #plt.title("Evaluacion de la duracion del servicio hasta la salida del cliente")
    plt.show()


def simulaciones():
    eleccion_Grafica = ""
    x = []; y = []
    print("==============================================")
    print("             MENÚ DE MM1                 ")
    print("==============================================")
    while eleccion_Grafica != "3":
        eleccion_Grafica = input("\n\t1. Sistema de colas MM1\n\t2. Linea de Espera\n\t\n\t3. Salir\n\tElija: ")
        if eleccion_Grafica == "1":
            mm1()
        elif eleccion_Grafica == "2":
            lineaDeEspera()
simulaciones()