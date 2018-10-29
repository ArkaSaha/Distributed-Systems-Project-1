from collections import deque
import sys
from random import choice, sample
from copy import deepcopy

def fn1(adj,c):
	s = 0
	for u in c:
		for v in adj[u]:
			if v in c:
				s += 1
	return s

def fn2(adj,u,c):
	s = 0
	for v in adj[u]:
		if v in c:
			s += 1
	return s

# Find Bridge Ends by RFST
def bridge_ends(adj,c,s_r):
	b = set()
	for u in s_r:
		q = deque()
		q.append(u)
		visited = set()
		while not (not q):
			v = q.popleft()
			visited.add(v)
			if v not in c:
				b.add(v)
			else:
				for w in adj[v]:
					if w not in visited and w not in s_r:
						q.append(w)
	return b

# Find sigma(s)
def sigma(adj,s_r,s_p,b):
	pb = set()
	for v in s_p:
		q = deque()
		q.append(v)
		visited = set()
		while not (not q):
			u = q.popleft()
			visited.add(u)
			if u in b:
				pb.add(u)
			else:
				for w in adj[u]:
					if w not in visited:
						q.append(w)
	return len(pb)

# Algorithm 1
def greedy_opoao(adj,c,s_r,alpha,b):
	s_p = set()
	s = 0
	while s<alpha*len(b):
		u = -1
		n = 0
		for v in set(adj.keys())-(s_p|s_r):
			ss = sigma(adj,s_r,s_p|set([v]),b)-s
			if ss>n:
				n = ss
				u = v
		s_p.add(u)
		s += n
	return s_p

# Algorithm 2
def greedy_scbg(b,q,sw):
	l = set()
	w = set()
	while len(l)<len(b):
		u = -1
		s = 0
		for v in sw:
			d = len(sw[v]-l)
			if d>=s:
				s = d
				u = v
		w.add(u)
		l.update(sw[u])
	return w

# Algorithm 3
def scbg_select(adj,c,s_r,b):
	q = {}
	for v in b:
		q[v] = set()
		m_d = sys.maxsize
		qq = deque()
		visited = set()
		qq.append((v,0))
		while not (not qq):
			u,d = qq.popleft()
			visited.add(u)
			q[v].add(u)
			if d<m_d:
				for w in adj[u]:
					if w in s_r:
						m_d = d+1
					if w not in visited:
						qq.append((w,d+1))
	sw = {}
	for v in q:
		for u in q[v]-s_r:
			if u not in sw:
				sw[u] = set()
			for w in q:
				if w!=v and u in q[w]:
					sw[u].add(w)
	return greedy_scbg(b,q,sw)

# 2nd Heuristic
def proximity(adj,s_r,size):
	s = set()
	for v in s_r:
		s.update(adj[v])
	return set(sample(s,size))

# 1st Heuristic
def max_degree(adj,size):
	l = sorted(adj.items(),key=lambda t: len(t[1]))
	return set([t[0] for t in l[-size:]])

# Read Graph
file = open('ca-HepTh.txt','r')
adj = {}
for i in range(4):
	line = file.readline()
m = 51975
for i in range(m):
	line = file.readline()
	l = line.split('\t')
	u = int(l[0])
	v = int(l[1])
	if u not in adj:
		adj[u] = set()
	adj[u].add(v)
file.close()

# Find communities
comm = {}
mem = {}
for i in adj:
	comm[i] = i
	mem[i] = set([i])
for u in adj:
	n = -1
	g = 0
	k_u = len(adj[u])
	for v in adj[u]:
		c = mem[comm[v]]
		s_in = fn1(adj,c)
		s_tot = sum([len(adj[w]) for w in c])
		k_u_in = fn2(adj,u,c)
		gain = ((s_in+2*k_u_in)/(2*m)-((s_tot+k_u)/(2*m))**2)-(s_in/(2*m)-(s_tot/(2*m))**2-(k_u/(2*m))**2)
		if g<gain:
			g = gain
			n = v
	if g>0:
		mem[comm[u]].discard(u)
		comm[u] = comm[n]
		mem[comm[n]].add(u)
for c in mem:
	if not (not mem[c]):
		print(mem[c])

# Find rumor originators and bridge ends
fc = open('comm_hep-th.txt','r')
comm = []
for i in range(3412):
	line = fc.readline()
	l = line.lstrip('{').rstrip('}\n').split(', ')
	c = set([int(j) for j in l])
	comm.append(c)
fc.close()
co = set()
while len(co)<100:
	co = choice(comm)
print(co)
s_r = set(sample(co,int(0.05*len(co))))
print(s_r)
b = bridge_ends(adj,co,s_r)
print(b)

# OPOAO
s_p1 = greedy_opoao(adj,co,s_r,0.6,b)
print(s_p1)
s_p2 = proximity(adj,s_r,len(s_p1))
print(s_p2)
s_p3 = max_degree(adj,len(s_p1))
print(s_p3)
f1 = open('hepTh_opoao_greedy.txt','w')
for i in range(100):
	infected = deepcopy(s_r)
	protected = deepcopy(s_p1)
	f1.write(str(len(infected))+' ')
	for j in range(31):
		pro = set()
		inf = set()
		for v in protected:
			w = choice(list(adj[v]))
			if w not in infected:
				pro.add(w)
		for v in infected:
			w = choice(list(adj[v]))
			if w not in protected and w not in pro:
				inf.add(w)
		protected.update(pro)
		infected.update(inf)
		f1.write(str(len(infected))+' ')
	f1.write('\n')
f1.close()
f2 = open('hepTh_opoao_proximity.txt','w')
for i in range(100):
	infected = deepcopy(s_r)
	protected = deepcopy(s_p2)
	f2.write(str(len(infected))+' ')
	for j in range(31):
		pro = set()
		inf = set()
		for v in protected:
			w = choice(list(adj[v]))
			if w not in infected:
				pro.add(w)
		for v in infected:
			w = choice(list(adj[v]))
			if w not in protected and w not in pro:
				inf.add(w)
		protected.update(pro)
		infected.update(inf)
		f2.write(str(len(infected))+' ')
	f2.write('\n')
f2.close()
f3 = open('hepTh_opoao_maxdegree.txt','w')
for i in range(100):
	infected = deepcopy(s_r)
	protected = deepcopy(s_p3)
	f3.write(str(len(infected))+' ')
	for j in range(31):
		pro = set()
		inf = set()
		for v in protected:
			w = choice(list(adj[v]))
			if w not in infected:
				pro.add(w)
		for v in infected:
			w = choice(list(adj[v]))
			if w not in protected and w not in pro:
				inf.add(w)
		protected.update(pro)
		infected.update(inf)
		f3.write(str(len(infected))+' ')
	f3.write('\n')
f3.close()
f4 = open('hepTh_opoao_noblocking.txt','w')
for i in range(100):
	infected = deepcopy(s_r)
	f4.write(str(len(infected))+' ')
	for j in range(31):
		inf = set()
		for v in infected:
			w = choice(list(adj[v]))
			inf.add(w)
		infected.update(inf)
		f4.write(str(len(infected))+' ')
	f4.write('\n')
f4.close()

# DOAM
s_p1 = scbg_select(adj,co,s_r,b)
print(s_p1)
s_p2 = proximity(adj,s_r,len(s_p1))
print(s_p2)
s_p3 = max_degree(adj,len(s_p1))
print(s_p3)
f1 = open('hepTh_doam_greedy.txt','w')
infected = deepcopy(s_r)
protected = deepcopy(s_p1)
infect = deepcopy(s_r)
protect = deepcopy(s_p1)
f1.write(str(len(infected))+' ')
for j in range(31):
	pro = set()
	inf = set()
	for v in protect:
		for w in adj[v]:
			if w not in infected:
				pro.add(w)
	for v in infect:
		for w in adj[v]:
			if w not in protected and w not in pro:
				inf.add(w)
	protect = pro
	infect = inf
	protected.update(pro)
	infected.update(inf)
	f1.write(str(len(infected))+' ')
f1.write('\n')
f1.close()
f2 = open('hepTh_doam_proximity.txt','w')
infected = deepcopy(s_r)
protected = deepcopy(s_p2)
infect = deepcopy(s_r)
protect = deepcopy(s_p1)
f2.write(str(len(infected))+' ')
for j in range(31):
	pro = set()
	inf = set()
	for v in protect:
		for w in adj[v]:
			if w not in infected:
				pro.add(w)
	for v in infect:
		for w in adj[v]:
			if w not in protected and w not in pro:
				inf.add(w)
	protect = pro
	infect = inf
	protected.update(pro)
	infected.update(inf)
	f2.write(str(len(infected))+' ')
f2.write('\n')
f2.close()
f3 = open('hepTh_doam_maxdegree.txt','w')
infected = deepcopy(s_r)
protected = deepcopy(s_p3)
infect = deepcopy(s_r)
protect = deepcopy(s_p1)
f3.write(str(len(infected))+' ')
for j in range(31):
	pro = set()
	inf = set()
	for v in protect:
		for w in adj[v]:
			if w not in infected:
				pro.add(w)
	for v in infect:
		for w in adj[v]:
			if w not in protected and w not in pro:
				inf.add(w)
	protect = pro
	infect = inf
	protected.update(pro)
	infected.update(inf)
	f3.write(str(len(infected))+' ')
f3.write('\n')
f3.close()
f4 = open('hepTh_doam_noblocking.txt','w')
infected = deepcopy(s_r)
infect = deepcopy(s_r)
f4.write(str(len(infected))+' ')
for j in range(31):
	inf = set()
	for v in infect:
		for w in adj[v]:
			inf.add(w)
	infect = inf
	infected.update(inf)
	f4.write(str(len(infected))+' ')
f4.write('\n')
f4.close()
