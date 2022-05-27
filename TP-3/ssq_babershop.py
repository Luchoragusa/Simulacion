'''
Owner : Hritik Jaiswal
Date : Nov 26 2020
Topic : To simulate a Single Server Queuing System (One-operator Barbershop problem) using Python
Subject : Modeling and simulation
https://gist.github.com/hritik5102/b2c14e831f03d7bf992e8ecf8a457bfd
'''

import random 

# Seed 
#random.seed(10)

# No. of Customer
size = 10

# Series of customer
customer = [i for i in range(1,size+1)]

# Inter Arrival Time (IAT)
inter_arrival_time = [random.randrange(1,10) for i in range(size)]

# Service Time 
service_time = [random.randrange(1,10) for i in range(size)]

print(len(inter_arrival_time),len(service_time))

# Calculate arrival time  (AT)
arrival_time = [0 for i in range(size)]

# initial 
arrival_time[0] = inter_arrival_time[0]

for i in range(1,size):
  arrival_time[i] = inter_arrival_time[i]+arrival_time[i-1]
 

Time_Service_Begin = [0 for i in range(size)]
Time_Customer_Waiting_in_Queue = [0 for i in range(size)]
Time_Service_Ends = [0 for i in range(size)]
Time_Customer_Spend_in_System = [0 for i in range(size)]
System_ideal = [0 for i in range(size)]

Time_Service_Begin[0] = arrival_time[0]
Time_Service_Ends[0] = service_time[0]
Time_Customer_Spend_in_System[0] = service_time[0]
for i in range(1,size):
  # Time Service Begin (TSB)
  Time_Service_Begin[i] = max(arrival_time[i],Time_Service_Ends[i-1])

  # Time customer waiting in queue (TCWQ)
  Time_Customer_Waiting_in_Queue[i] = Time_Service_Begin[i]-arrival_time[i]

  # Time service ends (TSE)
  Time_Service_Ends[i] = Time_Service_Begin[i] + service_time[i]  

  # Time Customer Spend in the system (TCSS)
  Time_Customer_Spend_in_System[i] = Time_Service_Ends[i] - arrival_time[i]

  # Time when system remains ideal (System Ideal)
  if (arrival_time[i]>Time_Service_Ends[i-1]):
    System_ideal[i] = arrival_time[i]-Time_Service_Ends[i-1]
  else:
    System_ideal[i] = 0 
    

from prettytable import PrettyTable

x = PrettyTable()

column_names = ['Customer','IAT','AT','ST','TSB','TCWQ','TSE','TCSS','System Ideal']
data = [customer,inter_arrival_time,arrival_time,service_time, Time_Service_Begin, Time_Customer_Waiting_in_Queue, Time_Service_Ends, Time_Customer_Spend_in_System, System_ideal]

length = len(column_names)

for i in range(length):
  x.add_column(column_names[i],data[i])
  
print(x)

'''
Performance measure 
Average waiting time = Total time customer wait in queue (minutes) / total number of customers 
 
Probability of customer (Wait) = Number of customer who wait / total number of customer 
 
Probability of Idle server =  Total Idle time of  server /  total  runtime of simulation
 
Average time between arrival = sum of all time times between arrival / number of arrivals -1 
 
Average waiting time those who wait = total time customers wait in the queue / total no. of customer who wait 
 
Average time customer spent in the system  = total time customers customer spent in the system / total no. of customer 
'''

# Average waiting time 
Average_waiting_time = sum(Time_Customer_Waiting_in_Queue)/size 

# Probability of customer were waiting
no_customer_who_are_waiting = len(list(filter(lambda x:x>0,Time_Customer_Waiting_in_Queue)))

prob_customer_waiting = no_customer_who_are_waiting / size

# Average service time
Average_service_time = sum(service_time)/size

# Probability of idle server
prob_ideal_server = sum(System_ideal) / Time_Service_Ends[size-1]  

# Average time between arrival
Average_Time_Between_Arrival = arrival_time[size-1] / (len(arrival_time) - 1)

# Average waiting time those who wait
average_waiting_time = sum(Time_Customer_Waiting_in_Queue) / no_customer_who_are_waiting

# Average time customer spent in the system 
time_customer_spent = sum(Time_Customer_Spend_in_System)/size

print("Average waiting time : {:.2f}".format(Average_waiting_time))
print('-'*50)

print("Probability of customer were waiting : {:.2f}".format(prob_customer_waiting))
print('-'*50)

print("Average service time : {:.2f}".format(Average_service_time))

print('-'*50)

print("Probability of idle server : {:.2f}".format(prob_ideal_server))

print('-'*50)

print("Average Time Between Arrival : {:.2f}".format(Average_Time_Between_Arrival))
print('-'*50)

print("Average waiting time those who wait : {:.2f}".format(average_waiting_time))
print('-'*50)

print("Average time customer spent in the system : {:.2f}".format(time_customer_spent))