import matplotlib.pyplot as plt
import numpy as np
import random


def coinToss(): return random.randint(0,1)

def sim():
    for k in range(10000):
        val=coinToss()
        if val==0: break
    return k

def superSim(numIter=10000):
    mean=0
    for _ in range(numIter): mean+=sim()
    return mean/numIter



xs=[]
ys=[]
numIter=10000
for a in range(numIter):
    print(100*a/numIter,"%")
    xs.append(a)
    ys.append(superSim())

plt.plot(xs,ys)
plt.show()

