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

# l =  µ * 0.25                     
# l =  µ * 0.50                     
# l =  µ * 0.75                     
#l =  µ        # tenemos divisin por 0 vas a ser imposible ???              
l =  µ *1.25                 

# np.random.seed(ncust)  
inter_arrival_times = list(np.random.exponential(scale=1/l,size=ncust))
arrival_times= []  
service_times = [] 
finish_times = []  
arrival_times = [0 for i in range(ncust)]
finish_times = [0 for i in range(ncust)]
arrival_times[0]=round(inter_arrival_times[0],2)  

for i in range(1,ncust):
    arrival_times[i]=round((arrival_times[i-1]+inter_arrival_times[i]),2) 
        
service_times = list(np.random.exponential(scale=1/µ,size=ncust))

finish_times[0]=round((arrival_times[0]+service_times[0]),2)
    
for i in range(1,ncust):
    finish_times[i] = round((max(arrival_times[i], finish_times[i-1]) + service_times[i]),2)

total_times =[abs(round((finish_times[i]-arrival_times[i]),2)) for i in range(ncust)]

wait_times = [abs(round((total_times[i] - service_times[i]),2)) for i in range(ncust)]

data = pd.DataFrame(list(zip(arrival_times,service_times,total_times,finish_times,wait_times,inter_arrival_times)),columns =['arrival_times', 'service_times','total_times','finish_times','wait_times','inter_arrival_times']) 

tbe=list([0])
timeline=['simulation starts']
for i in range(1,ncust):
    tbe.append(data['arrival_times'][i])
    tbe.append(data['finish_times'][i])
    timeline.append('customer ' +str(i)+' arrived')
    timeline.append('customer ' +str(i)+' left')

timeline = pd.DataFrame(list(zip(tbe,timeline)), 
columns =['time','Timeline']).sort_values(by='time').reset_index()
timeline=timeline.drop(columns='index')

timeline['n']=0  
x=0
idletime=0
workingtime=0

for i in range(1,(2*ncust)-2):
    if len( (  (timeline.Timeline[i]).split() ) )>2:
        z=str(timeline['Timeline'][i]).split()[2]
    else:
        continue
    if z =='arrived':
        x = x+1
        timeline['n'][i]=x
    else:
        x=x-1
    if x==-1:
        x=0
    timeline['n'][i]=x

    if timeline['n'][i]==0:
        idletime=idletime+ timeline['time'][i+1]-timeline['time'][i]
    else:
        workingtime= workingtime+ timeline['time'][i+1]-timeline['time'][i]

workingtime=workingtime+timeline['time'][2*ncust-3]-timeline['time'][2*ncust-2] 

timeline.time.max()
workingtime+idletime

data['occupied']=[0 for i in range(ncust)]

for i in range(1,ncust):    
    if data.arrival_times[i]>data.finish_times[i-1]:
        data['occupied'][i]=1
    else:
        data['occupied'][i]=0
        
t= list()
for i in timeline.index: 
    if i == (2*ncust) -2 :
        continue
    x=timeline.time[i+1]
    y=timeline.time[i]
    t.append(round((x-y),3))

t.append(0) 
timeline['tbe']=t
Pn=timeline.groupby('n').tbe.agg(sum)/sum(t)

timeline.n.describe()  
data.occupied.value_counts()  

timeline['Lq']=0  
for i in timeline.index:
    if timeline.n[i]>1:
        timeline.Lq[i]= timeline['n'][i]-c

ocupation= pd.Series(name='ocupation',data=[idletime/data.finish_times.max(), workingtime/data.finish_times.max()],index=['Libre','Ocupado'])
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

Ls=(sum(Pn*Pn.index)) 
Lq=sum((Pn.index[c+1:]-1)*(Pn[c+1:]))
print('\nSALIDAS:','\n',
    'Tiempo entre arrivos : ',str(data.inter_arrival_times.mean()),'  ---------------------------- Valor Teorico : ', 1/l ,'\n',
    'Tiempo de servicio: (1/µ)',str(data.service_times.mean()),'  ---------------------------- Valor Teorico : ',1/µ,'\n'
    'Numero esperado de clientes en el sistema(Ls):',str(Ls),  '  ---------------------------- Valor Teorico : ', l/(µ-l) ,'\n',
    'Numero esperado de clientes en linea (Lq):',str(Lq),'Valor Teorico : ', l*l/µ*(µ-l) ,'\n',
    'Tiempo previsto de permanencia en el sistema (Ws):',str(data.total_times.mean()),' --------------------------------- Valor Teorico : ', 1/(µ-l) ,'\n',
    'Tiempo esperado en linea (Wq):',str(data['wait_times'].mean()),' --------------------------------        Valor Teorico : ', l/µ*(µ-l) ,'\n',
    'Utilizacion (c): ',str(workingtime/timeline.time.max()),' ------------------------- Valor Teorico : ', l/µ ,'\n\n',
    'Po: ',Pn[0],' ------------------------- Valor Teorico : ',1- l/µ ,'\n\n',
    'Probabilidad que haya n clientes en el sistema :',Pn,'\n')

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

