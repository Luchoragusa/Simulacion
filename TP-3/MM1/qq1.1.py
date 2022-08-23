import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

l = 2                
µ = 3                    
ncust =1000         
c=1  

# =============================================
'Variacion de porcentajes de lambda y mu'
l =  µ * 0.25                     
# l =  µ * 0.50                     
# l =  µ * 0.75                     
# l =  µ        
# l =  µ *1.25                 
# =============================================

inter_arrival_times = list(np.random.exponential(scale=1/l,size=ncust))  # lista de tiempos de llegada de los clientes, exponencial con media 1/l y tamaño = numero de clientes
arrival_times= []  
service_times = [] 
finish_times = []  
arrival_times = [0 for i in range(ncust)]       
finish_times = [0 for i in range(ncust)]    
arrival_times[0]=round(inter_arrival_times[0],2)    

for i in range(1,ncust):    
    arrival_times[i]=round((arrival_times[i-1]+inter_arrival_times[i]),2)   # tiempo de llegada de los clientes = tiempo de llegada anterior + tiempo de llegada actual

service_times = list(np.random.exponential(scale=1/µ,size=ncust))   # lista de tiempos de servicio de los clientes, exponencial con media 1/µ y tamaño = numero de clientes

finish_times[0]=round((arrival_times[0]+service_times[0]),2)    # tiempo de finalizacion del primer cliente = tiempo de llegada del primer cliente + tiempo de servicio del primer cliente

for i in range(1,ncust):
    finish_times[i] = round((max(arrival_times[i], finish_times[i-1]) + service_times[i]),2)    # tiempo de finalizacion del cliente i = max(tiempo de llegada del cliente i, tiempo de finalizacion del cliente i-1) + tiempo de servicio del cliente i

total_times =[abs(round((finish_times[i]-arrival_times[i]),2)) for i in range(ncust)]   # lista de tiempos totales de los clientes, abs(tiempo de finalizacion - tiempo de llegada)

wait_times = [abs(round((total_times[i] - service_times[i]),2)) for i in range(ncust)]  # lista de tiempos de espera de los clientes, abs(tiempo total - tiempo de servicio)

data = pd.DataFrame(list(zip(arrival_times,service_times,total_times,finish_times,wait_times,inter_arrival_times)),columns =['arrival_times', 'service_times','total_times','finish_times','wait_times','inter_arrival_times'])     
# en data se guarda un dataframe con los tiempos de llegada, tiempo de servicio, tiempo total, tiempo de finalizacion, tiempo de espera y tiempo de llegada de los clientes
# un DataFrame es una tabla de datos con n columnas y m filas

tbe=list([0]) 
timeline=['simulation starts']  
for i in range(1,ncust):
    tbe.append(data['arrival_times'][i])    
    tbe.append(data['finish_times'][i])
    timeline.append('customer ' +str(i)+' arrived')
    timeline.append('customer ' +str(i)+' left')
# se guardan los tiempos de espera acumulados de los clientes en tbe y en timeline (llegada y salida de los clientes)

timeline = pd.DataFrame(list(zip(tbe,timeline)),    # DataFrame(list(zip(tbe,timeline)) es un dataframe con dos columnas, la primera con los tiempos de espera acumulados y la segunda con los eventos que ocurrieron
columns =['time','Timeline']).sort_values(by='time').reset_index() # se ordena el dataframe por el tiempo de espera acumulado y se resetea el indice
timeline=timeline.drop(columns='index') # se elimina la columna index

timeline['n']=0  
x=0
idletime=0
workingtime=0

for i in range(1,(2*ncust)-2):   
    if len(((timeline.Timeline[i]).split()))>2:    # len(((timeline.Timeline[i]).split() ) )>2 es una condicion que determina si el evento ocurrio o no (si el evento ocurrio, la longitud de la lista es 3, si no, es 2) 
        z=str(timeline['Timeline'][i]).split()[2]   # se guarda el evento en z (llegada o salida del cliente) 
    else:
        continue
    if z =='arrived':   # si el evento es llegada del cliente, se agrega uno a la columna n de la fila en la que se encuentra el evento
        x = x+1 # x=x+1 quiere decir que el cliente x llego a la cola 
        timeline['n'][i]=x 
    else:
        x=x-1   # si el evento es salida del cliente, se resta uno a la columna n de la fila en la que se encuentra el evento
    if x==-1:   
        x=0 # x=0 quiere decir que el servidor esta libre y no hay clientes en espera
    timeline['n'][i]=x

    if timeline['n'][i]==0:
        idletime=idletime+ timeline['time'][i+1]-timeline['time'][i]    # en idletime se guarda el tiempo de espera acumulado del servidor cuando esta libre 
    else:
        workingtime= workingtime+ timeline['time'][i+1]-timeline['time'][i]   # en workingtime se guarda el tiempo de espera acumulado del servidor cuando hay clientes en espera

workingtime=workingtime+timeline['time'][2*ncust-3]-timeline['time'][2*ncust-2]     # se vuelve a sumar el tiempo de espera acumulado del servidor cuando el ultimo cliente llego a la cola y se termino de atender

timeline.time.max() # se guarda el tiempo maximo de espera acumulado de los clientes
workingtime+idletime    

data['occupied']=[0 for i in range(ncust)]  # data['occupied'] se guarda una lista de 0's con el tamaño de la lista de los clientes

for i in range(1,ncust):    
    if data.arrival_times[i]>data.finish_times[i-1]:    # si el tiempo de llegada del cliente i es mayor al tiempo de finalizacion del cliente i-1
        data['occupied'][i]=1   # el cliente i esta ocupado
    else:
        data['occupied'][i]=0   # el cliente i no esta ocupado
        
t= list()   
for i in timeline.index:    
    if i == (2*ncust) -2 :  # si el indice es el ultimo indice de timeline
        continue
    x=timeline.time[i+1]    # x es el tiempo del evento siguiente 
    y=timeline.time[i]      # y es el tiempo del evento actual
    t.append(round((x-y),3))    # se guarda el tiempo de espera acumulado del cliente en t, redondeado a 3 decimales

t.append(0) 
timeline['tbe']=t   
Pn=timeline.groupby('n').tbe.agg(sum)/sum(t)  
# se calcula el promedio de tiempo de espera acumulado de los clientes en la cola, dividiendo el tiempo de espera acumulado de los clientes en la cola por el tiempo de espera acumulado total de los clientes en la cola


timeline.n.describe()  
# se calcula la media, la desviacion estandar y el maximo de la cola de clientes
data.occupied.value_counts()  
# se calcula la cantidad de clientes que estan ocupados y no estan ocupados

timeline['Lq']=0  
# se crea una columna para guardar el tiempo de espera acumulado de los clientes en la cola
for i in timeline.index:    
    if timeline.n[i]>1:   # si el cliente esta en la cola 
        timeline.Lq[i]= timeline['n'][i]-c  # se guarda el tiempo de espera acumulado del cliente en la cola 
        # c es la capacidad de la cola

ocupation= pd.Series(name='ocupation',data=[idletime/data.finish_times.max(), workingtime/data.finish_times.max()],index=['Libre','Ocupado'])
# se calcula la ocupacion del servidor, dividiendo el tiempo de espera acumulado del servidor libre por el tiempo de espera acumulado total del servidor y dividiendo el tiempo de espera acumulado del servidor ocupado por el tiempo de espera acumulado total del servidor
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# se imprime la ocupacion del servidor y la cantidad de clientes que estan ocupados y no estan ocupados en la cola

# =========================================================
#             Valor esperado y calculado/teórico
# =========================================================
Ls=(sum(Pn*Pn.index))   # se calcula el tiempo de espera acumulado de los clientes en la cola
Lq=sum((Pn.index[c+1:]-1)*(Pn[c+1:]))   # se calcula el tiempo de espera acumulado de los clientes en la cola
print('\nSALIDAS:','\n',    
    'Tiempo entre arrivos : ',str(data.inter_arrival_times.mean()),'  ------------------------> Valor Teorico : ', 1/l ,'\n',    
    'Tiempo de servicio: (1/µ)',str(data.service_times.mean()),'  ----------------------------> Valor Teorico : ',1/µ,'\n'
    'Numero esperado de clientes en el sistema(Ls):',str(Ls),  '  ----------------------------> Valor Teorico : ', l/(µ-l) ,'\n',
    'Numero esperado de clientes en linea (Lq):',str(Lq),' -----------------------------------> Valor Teorico : ', l*l/µ*(µ-l) ,'\n',
    'Tiempo previsto de permanencia en el sistema (Ws):',str(data.total_times.mean()),' ------> Valor Teorico : ', 1/(µ-l) ,'\n',
    'Tiempo esperado en linea (Wq):',str(data['wait_times'].mean()),' ------------------------> Valor Teorico : ', l/µ*(µ-l) ,'\n',
    'Utilizacion (c): ',str(workingtime/timeline.time.max()),' -------------------------------> Valor Teorico : ', l/µ ,'\n',
    'Probabilidad de que el sistema esté desocupado (Po): ',Pn[0],' --------------------------> Valor Teorico : ',1- l/µ ,'\n\n',
    'Probabilidad que haya n clientes en el sistema :',Pn,'\n')


# =========================================================
#                       Graficas
# =========================================================
plt.figure(figsize=(12,4))
sns.lineplot(x=data.index,y=wait_times,color='black')
plt.xlabel('Numeros de clientes')  
plt.ylabel('Minutos')
plt.title('Tiempo de espera de los clientes') 

plt.figure(figsize=(7,7))
sns.distplot(inter_arrival_times,kde=False,color='r')
plt.title('Tiempo entre arribos')
plt.xlabel('Minutos')
plt.ylabel('Frecuencia')

plt.figure(figsize=(8,8))
sns.distplot(service_times,kde=False)
plt.title('Tiempos de servicio')
plt.xlabel('Minutos') 
plt.ylabel('Frecuencia')

plt.figure(figsize=(8,8))
sns.barplot(x=Pn.index,y=Pn,color='g')
plt.title('Probabilidad de n clientes en el sistema')
plt.xlabel('Numero de clientes')
plt.ylabel('Probabilidad')

plt.figure(figsize=(7,7))
sns.barplot(ocupation.index,ocupation,color='mediumpurple')
plt.title('Utilización %')
plt.xlabel('Estado del Sistema')
plt.ylabel('Probabilidad')

plt.show()