import numpy as np
import random

layers=[2,3,2]

def rand(): return random.randint(-300,300)/100

Ws=[]
Bs=[]
Bst=[]
for i in range(len(layers)-1):
    Wi=np.array([[rand() for _ in range(layers[i+1])] for _ in range(layers[i])])
    Ws.append(Wi)
    Bi=np.transpose(np.array([rand() for _ in range(layers[i+1])]))
    Bs.append(Bi)
    Bit=np.array([rand() for _ in range(layers[i+1])])
    Bst.append(Bit)

def Sigmoid(vector):
    return (2/(1+np.exp(-vector)))-1

print("Ws:")
for W in Ws: print("*",W)
print("Bs:")
for B in Bs: print("*",B)

I0=np.array([3,2])
print("I0:",I0)
Is=[I0]
for i in range(len(layers)-1):
    Ii1=(Is[i]@Ws[i])+Bs[i]
    Is.append(Sigmoid(Ii1))

print("Is:")
for I in Is: print("*",I)

W0=[
    [1,2,3],
    [4,5,6]    
]
W0=np.array(W0)
B0=[13,14,15]
B0=np.transpose(np.array(B0))
I0=[18,19]
I0=np.array(I0)

I1p=(I0@W0)
I1=I1p+B0

print("I1p:",I1p)
print("I1:",I1)
