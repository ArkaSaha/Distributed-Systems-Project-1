import numpy as np
import matplotlib.pyplot as plt

# OPOAO
file = open('hepTh_opoao_greedy.txt','r')
m1 = []
for i in range(100):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m1.append(n)
file.close()
y1 = np.mean(np.array(m1),axis=0)
file = open('hepTh_opoao_maxdegree.txt','r')
m2 = []
for i in range(100):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m2.append(n)
file.close()
y2 = np.mean(np.array(m2),axis=0)
file = open('hepTh_opoao_proximity.txt','r')
m3 = []
for i in range(100):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m3.append(n)
file.close()
y3 = np.mean(np.array(m3),axis=0)
file = open('hepTh_opoao_noblocking.txt','r')
m4= []
for i in range(100):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m4.append(n)
file.close()
y4 = np.mean(np.array(m4),axis=0)
x = range(32)
plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)
plt.plot(x,y4)
plt.title('OPOAO HepTh')
plt.xlabel('Number of Hops')
plt.ylabel('Number of Infected Nodes')
plt.legend(['Greedy','Max Degree','Proximity','No Blocking'])
plt.show()

# DOAM
file = open('hepTh_doam_greedy.txt','r')
m1 = []
for i in range(1):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m1.append(n)
file.close()
y1 = np.mean(np.array(m1),axis=0)
file = open('hepTh_doam_maxdegree.txt','r')
m2 = []
for i in range(1):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m2.append(n)
file.close()
y2 = np.mean(np.array(m2),axis=0)
file = open('hepTh_doam_proximity.txt','r')
m3 = []
for i in range(1):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m3.append(n)
file.close()
y3 = np.mean(np.array(m3),axis=0)
file = open('hepTh_doam_noblocking.txt','r')
m4= []
for i in range(1):
	line = file.readline()
	l = line.split(' ')
	n = []
	for j in l[0:-1]:
		n.append(int(j))
	m4.append(n)
file.close()
y4 = np.mean(np.array(m4),axis=0)
x = range(32)
plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)
plt.plot(x,y4)
plt.title('DOAM HepTH')
plt.xlabel('Number of Hops')
plt.ylabel('Number of Infected Nodes')
plt.legend(['Greedy','Max Degree','Proximity','No Blocking'])
plt.show()