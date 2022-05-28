import random as ran
import math
import simpy as sim
import matplotlib.pyplot as plt

#===============================================================================================
#                                       MM1
#===============================================================================================
def mm1():
    titulo = 'Sistema de colas MM1'
    print(titulo.center(80, '='))
    for i in range(10):    
        mu = ran.randint(5,10)                                  # el promedio de clientes atendidos por hora
        lambdas = [mu*0.25, mu*0.5, mu*0.75, mu, mu*1.25]         # el promedio de clientes por hora  
        for j in range(len(lambdas)):
            if mu > lambdas[j]:
                Ls = lambdas[j]/(mu-lambdas[j])
                Ws = 1/(mu-lambdas[j])
                Wsl = Ws*60
                Lq = Ls*lambdas[j]/mu
                Wq = Ws*lambdas[j]/mu
                Wql = Wq*60
                pu = lambdas[j]/mu
                po = 1 - pu
                pe = (1 - (lambdas[j]/mu)) * ((lambdas[j]/mu) * (lambdas[j]/mu))

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

                trafico = lambdas[j]/mu
                Cperdidos = trafico/(trafico+1)
                print(f"Porcentaje de perdidos: {Cperdidos*100} %")

                print("Si el horario de atencion consta de 8 horas")
                totalC = mu*8
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
        
        #plt.bar(clientes[i], round(tiempo_espera[i],2))     # Evaluacion del tiempo de espera de cada cliente (en cola)
        #plt.bar(clientes[i], clientes_en_sistema[i])        # Evaluacion de clientes en el sistema
    
    plt.xlabel("Numero de repeticiones")
    plt.ylabel("Resultados")
    #plt.title("Evaluacion del tiempo de espera de cada cliente")
    #plt.title("Evaluacion de clientes en el sistema")
    plt.show()

#===============================================================================================
#                               Simulacion usando simpy
#===============================================================================================
'''Explicacion:
        Una peluqueria tiene un peluquero que se demora entre 15 y 30 minutos por corte. La peluqueria recibe en promedio 3 clientes
        por hora (o sea, uno cada 20 minutos). Se simula las llegadas y servicios de 5 clientes

        Se puede variar cualquier parametro (n peluqueros, cambiar tiempo en que se demora por corte, n clientes, X tiempo especifico)

    Valor teorico esperado
        Los numeros pseudoaleatorios que utilizaremos seran los siguientes: 
        0.5391, 0.2892, 0.6536, 0.2573, 0.6416, 0.0300, 0.2100, 0.3972, 0.9888, 0.4615
        https://naps.com.mx/blog/simulacion-en-python-usando-simpy/
'''
def cortar(cliente):
	global dt  #Para poder acceder a la variable dt declarada anteriormente
	R = ran.random()  # Obtiene un numero aleatorio y lo guarda en R
	tiempo = TIEMPO_CORTE_MAX - TIEMPO_CORTE_MIN  
	tiempo_corte = TIEMPO_CORTE_MIN + (tiempo*R) # Distribucion uniforme
	yield env.timeout(tiempo_corte) # deja correr el tiempo n minutos
	print(" \o/ Corte listo a %s en %.2f minutos" % (cliente,tiempo_corte))
	dt = dt + tiempo_corte # Acumula los tiempos de uso de la i

def cliente (env, name, personal ):
	global te
	global fin
	llega = env.now # Guarda el minuto de llegada del cliente
	print ("---> %s llego a peluqueria en minuto %.2f" % (name, llega))
	with personal.request() as request: # Espera su turno
		yield request # Obtiene turno
		pasa = env.now # Guarda el minuto cuado comienza a ser atendido
		espera = pasa - llega # Calcula el tiempo que espero
		te = te + espera # Acumula los tiempos de espera
		print ("**** %s pasa con peluquero en minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
		yield env.process(cortar(name)) # Invoca al proceso cortar
		deja = env.now #Guarda el minuto en que termina el proceso cortar 
		print ("<--- %s deja peluqueria en minuto %.2f" % (name, deja))
		fin = deja # Conserva globalmente el ultimo minuto de la simulacion
	
def principal (env, personal):
	llegada = 0
	i = 0
	for i in range(TOT_CLIENTES): # Para n clientes
		R = ran.random()
		llegada = -T_LLEGADAS * math.log(R) # Distribucion exponencial
		yield env.timeout(llegada)  # Deja transcurrir un tiempo entre uno y otro
		i += 1
		env.process(cliente(env, 'Cliente %d' % i, personal)) 

SEMILLA = 30
NUM_PELUQUEROS = 1
TIEMPO_CORTE_MIN = 15
TIEMPO_CORTE_MAX = 30
T_LLEGADAS = 20
TIEMPO_SIMULACION = 120
TOT_CLIENTES = 5
te  = 0.0 # tiempo de espera total
dt  = 0.0 # duracion de servicio total
fin = 0.0 # minuto en el que finaliza

'''
titulo = 'Simulacion Peluqueria'
print(titulo.center(80, '='))
ran.seed(SEMILLA)   # cualquier valor
env = sim.Environment()   # crea el objeto entorno de simulacion
personal = sim.Resource(env, NUM_PELUQUEROS)     # crea los recursos (peluqueros)
env.process(principal(env, personal))       # invoca el proceso principal
env.run()
print("\n=============================================================")
print("\n Indicadores obtenidos: ")
lpc = te / fin
print("\nLongitud promedio de la cola: %.2f" % lpc)
tep = te / TOT_CLIENTES
print("Tiempo de espera promedio del total de clientes = %.2f" % tep)
upi = (dt / fin) / NUM_PELUQUEROS
print("Uso promedio del servidor = %.2f" % upi)
print("\n=============================================================")
'''

def simulaciones():
    eleccion_Grafica = ""
    x = []; y = []
    print("==============================================")
    print("             MENÚ DE MM1                 ")
    print("==============================================")
    while eleccion_Grafica != "8":
        eleccion_Grafica = input("\n\t1. Sistema de colas MM1\n\t2. Linea de Espera\n\t3. Simulacion usando simpy\n\t4. Salir\n\tElija: ")
        if eleccion_Grafica == "1":
            mm1()
        elif eleccion_Grafica == "2":
            lineaDeEspera()
        elif eleccion_Grafica == "3":   # Para ejecutar este, descomentar la linea 174 a 190
            principal()
simulaciones()