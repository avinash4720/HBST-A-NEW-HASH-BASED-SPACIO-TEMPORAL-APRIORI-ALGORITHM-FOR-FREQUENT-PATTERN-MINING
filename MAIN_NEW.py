# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 22:33:29 2021

@author: acer
"""

from FP_TREE_25th_Dec import *
from HBST_27th_Dec import *
import matplotlib.pyplot as plt
import numpy as np


''' printing time taken in each process for both HBST and FP-TREE '''


'''

#print('Total time taken in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', total_time_HBST.microseconds)
#print('Total time taken in (microseconds) by fptree algorithm:', total_time.microseconds)
print('Total time taken for preprocessing in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', preprocess_time_HBST.microseconds)
#print('Total time taken for CMS Generation in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', CMS_Generation_time_HBST.microseconds)

print('Total time taken for 2-Item-set in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', two_Item_set_time_HBST.microseconds)
print('Total time taken for star_Item-set in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', Star_Item_set_time_HBST.microseconds)
print('Total time taken for preprocessing in (microseconds) by FP-Tree algorithm:', preprocess_time.microseconds)
print('Total time taken for 2-Item-set in (microseconds) by FP-Tree algorithm:', two_Item_set_time.microseconds)
print('Total time taken for star_Item-set in (microseconds) by FP-Tree algorithm:', Star_Item_set_time.microseconds)

'''


#time=[str(total_time_HBST.total_seconds()),str(total_time.total_seconds())]
#algorithms=["HBST","FP-TREE"]

#x = np.array([int(str(preprocess_time_HBST.total_seconds())),str(two_Item_set_time_HBST.total_seconds()),str(Star_Item_set_time_HBST.total_seconds()) ])
#y = np.array([ 20, 30, 5, 12, 39, 48, 50, 3 ])
#print(Star_Item_set_time_HBST.microseconds)
#print(Star_Item_set_time_HBST.total_seconds())
#print(preprocess_time_HBST.total_seconds())


''' Plotting graph for Run-Time vs Algorithm '''


HBST_time=np.array([preprocess_time_HBST.microseconds,two_Item_set_time_HBST.microseconds,Star_Item_set_time_HBST.microseconds])
FP_TREE_time=np.array([preprocess_time.microseconds,two_Item_set_time.microseconds,Star_Item_set_time.microseconds])
STAGES=["Preprocessing","Final-Item-set","star-Item-set"]
plt.plot(STAGES, HBST_time, color='r', label='HBST')
plt.plot(STAGES , FP_TREE_time , color='g', label='FP-TREE')
#plt.plot(algorithms,time)
plt.xlabel('Algorithm')     
plt.ylabel('Run-Time')
plt.title('RUN-TIME vs ALGORITHM')
plt.legend()
plt.show()


''' Printing graph for Co-occuring Pollutant vs Time for Ahmedabad '''


individual=[]
co_occuring=[]
pollutants=[]

for id,itemset in Pollutant_Max_Freq.items():
    if itemset[0][0][0] == "Ahmedabad":
        individual.append(itemset[1])
        co_occuring.append(itemset[0][2])
        pollutants.append(itemset[0][1])
individual.pop()
co_occuring.pop()
#print(individual)
#print(co_occuring)

w=0.4
months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
bar1=np.arange(len(months))
bar2=[i+w for i in bar1]
plt.bar(bar1,co_occuring,w,label="Itemsets(co-occuring)Freq")
plt.bar(bar2,individual,w,label="Pollutants Individual Freq")

def addtext(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

#pollutants=[1,2,3,4,5,6,7,8,9,10,11,12]
#addtext(months,pollutants)  

plt.xlabel("Time(2015-2020)")
plt.ylabel("Frequency")
plt.title("Ahmedabad ")
plt.xticks(bar1+w/2,months)
plt.legend()
plt.show()


''' Printing graph for Co-occuring Pollutant vs Time for Chennai '''


individual=[]
co_occuring=[]
pollutants=[]

for id,itemset in Pollutant_Max_Freq.items():
    if itemset[0][0][0] == "Chennai":
        individual.append(itemset[1])
        co_occuring.append(itemset[0][2])
        pollutants.append(itemset[0][1])
individual.pop()
co_occuring.pop()
#print(individual)
#print(co_occuring)

w=0.4
months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
bar1=np.arange(len(months))
bar2=[i+w for i in bar1]
plt.bar(bar1,co_occuring,w,label="Itemsets(co-occuring)Freq")
plt.bar(bar2,individual,w,label="Pollutants Individual Freq")

def addtext(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

#pollutants=[1,2,3,4,5,6,7,8,9,10,11,12]
#addtext(months,pollutants)  

plt.xlabel("Time(2015-2020)")
plt.ylabel("Frequency")
plt.title("Chennai ")
plt.xticks(bar1+w/2,months)
plt.legend()
plt.show()


''' Printing graph for maximum Co-occuring Pollutant count vs Time for Delhi '''


individual=[]
co_occuring=[]
pollutants=[]

for id,itemset in Pollutant_Max_Freq.items():
    if itemset[0][0][0] == "Delhi":
        individual.append(itemset[1])
        co_occuring.append(itemset[0][2])
        pollutants.append(itemset[0][1])
individual.pop()
co_occuring.pop()
#print(individual)
#print(co_occuring)

w=0.4
months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
bar1=np.arange(len(months))
bar2=[i+w for i in bar1]
plt.bar(bar1,co_occuring,w,label="Itemsets(co-occuring)Freq")
plt.bar(bar2,individual,w,label="Pollutants Individual Freq")

def addtext(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

#pollutants=[1,2,3,4,5,6,7,8,9,10,11,12]
#addtext(months,pollutants)  

plt.xlabel("Time(2015-2020)")
plt.ylabel("Frequency")
plt.title("Delhi")
plt.xticks(bar1+w/2,months)
plt.legend()
plt.show()


''' Printing table for max Co-occuring pollutant with time for 3 major cities '''  


from prettytable import PrettyTable 
  
# Specify the Column Names while initializing the Table 
myTable = PrettyTable(["Time", "Itemset (Co-occuring Pollutants)", "Count"]) 
# Add rows 

print("\n\t\t\t\t\t\tAHMEDABAD\n")
for id,itemset in Pollutant_Max_Freq.items():
    if (itemset[0][0][0] == "Ahmedabad") & (itemset[0][0][1] != "*") :
        myTable.add_row([itemset[0][0][1],itemset[0][1],itemset[0][2]]) 
print(myTable)


myTable1 = PrettyTable(["Time", "Itemset (Co-occuring Pollutants)", "Count"]) 

print("\n\t\t\t\t\t\t CHENNAI\n")
for id,itemset in Pollutant_Max_Freq.items():
    if (itemset[0][0][0] == "Chennai") & (itemset[0][0][1] != "*") :
        myTable1.add_row([itemset[0][0][1],itemset[0][1],itemset[0][2]]) 
print(myTable1)

myTable2 = PrettyTable(["Time", "Itemset (Co-occuring Pollutants)", "Count"]) 

print("\n\t\t\t\t\t\tDELHI\n")
for id,itemset in Pollutant_Max_Freq.items():
    if (itemset[0][0][0] == "Delhi") & (itemset[0][0][1] != "*") :
        myTable2.add_row([itemset[0][0][1],itemset[0][1],itemset[0][2]]) 
print(myTable2)
