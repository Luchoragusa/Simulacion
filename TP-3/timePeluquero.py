import random as ran
import math
import simpy as sim

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
	while True: 
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
TIEMPO_SIMULACION = 220
TOT_CLIENTES = 5
te  = 0.0 # tiempo de espera total
dt  = 0.0 # duracion de servicio total
fin = 0.0 # minuto en el que finaliza

titulo = 'Simulacion Peluqueria'
print(titulo.center(80, '='))
ran.seed(SEMILLA)   # cualquier valor
env = sim.rt.RealtimeEnvironment(factor=1.0)   # crea el objeto entorno de simulacion
personal = sim.Resource(env, NUM_PELUQUEROS)     # crea los recursos (peluqueros)
env.process(principal(env, personal))       # invoca el proceso principal
env.run(until=TIEMPO_SIMULACION)
print("\n=============================================================")
print("\n Indicadores obtenidos: ")
lpc = te / fin
print("\nLongitud promedio de la cola: %.2f" % lpc)
tep = te / TOT_CLIENTES
print("Tiempo de espera promedio del total de clientes = %.2f" % tep)
upi = (dt / fin) / NUM_PELUQUEROS
print("Uso promedio del servidor = %.2f" % upi)
print("\n=============================================================")