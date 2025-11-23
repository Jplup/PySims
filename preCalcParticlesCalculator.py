import random
import numpy as np
import json
import time

WIDTH = 400
HEIGHT = 300

tooCloseDistance=5

particleSize=2
playbackSpeed=5

class Particle:
    def __init__(self,x,y,mass,randomVels,maxVel):
        self.x=x
        self.y=y
        self.maxVel=maxVel
        if randomVels:
            self.vx=random.randint(-5,5)
            self.vy=random.randint(-5,5)
        else:
            self.vx=0
            self.vy=0
        self.ax=0
        self.ay=0
        self.m=mass
        self.r=particleSize/2
        self.fx=0
        self.fy=0
        self.xs=[x]
        self.ys=[y]

    def SaturateValues(self,value):
        maximums=[-self.maxVel,self.maxVel]
        if value<maximums[0]: return maximums[0]
        if value>maximums[1]: return maximums[1]
        return value

    def update(self,dt):

        self.ax=self.fx/self.m
        self.vx+=self.ax*dt
        self.vx=self.SaturateValues(self.vx)
        self.x+=self.vx*dt

        self.ay=self.fy/self.m
        self.vy+=self.ay*dt
        self.vy=self.SaturateValues(self.vy)
        self.y+=self.vy*dt
        
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1

        self.xs.append(self.x)
        self.ys.append(self.y)

        self.fx=0
        self.fy=0

def CalculateForces(p1,p2,epsilon,sigma):
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    d=np.sqrt((dx**2)+(dy**2))
    if dx==0: dx=0.0001
    if dy==0: dy=0.0001
    F=(24*epsilon/(d**2))*(((sigma/d)**6)-(2*((sigma/d)**12)))

    return F*dx/d,F*dy/d

def UnZero(value):
    if value==0: return 0.0001
    else: return value

def ForceFromDistance(d,epsilon,sigma):
    return -(24*epsilon/(d**2))*(((sigma/d)**6)-(2*((sigma/d)**12)))

def CalculateSimulation(finalTime,dt,numParticles,mass,E,S,rVels,MV):
    particles=[]
    for _ in range(numParticles):
        for _ in range(100):
            x=random.random()*WIDTH
            y=random.random()*HEIGHT
            tooClose=False
            for other in particles:
                dx=x-other.x
                dy=y-other.y
                d=np.sqrt((dx**2)+(dy**2))
                if d<tooCloseDistance:
                    tooClose=True
                    break
            if not tooClose:
                particles.append(Particle(x,y,mass,rVels,MV))
                break

    time=np.linspace(0,finalTime,int(finalTime/dt))
    goals=[10,25,50,75,90]
    printGoal=[True for _ in goals]
    for k in range(int(finalTime/dt)):
        for i in range(numParticles):
            for j in range(numParticles-1-i):
                p1=particles[i]
                p2=particles[j+1+i]
                fx,fy=CalculateForces([p1.x,p1.y],[p2.x,p2.y],E,S)
                p1.fx+=fx
                p1.fy+=fy
                p2.fx-=fx
                p2.fy-=fy
        for p in particles:
            dxl=UnZero(p.x)
            dxr=UnZero(WIDTH-p.x)
            dyd=UnZero(p.y)
            dyu=UnZero(HEIGHT-p.y)
            Fx=ForceFromDistance(dxl,E,S)-ForceFromDistance(dxr,E,S)
            Fy=ForceFromDistance(dyd,E,S)-ForceFromDistance(dyu,E,S)
            p.fx+=Fx
            p.fy+=Fy
        for p in particles: p.update(dt)
        percet=round((100*k)/(int(finalTime/dt)),2)
        for aux,goal in enumerate(goals):
            if percet>goal and printGoal[aux]: 
                print("  ",percet,"%")
                printGoal[aux]=False
    particlePositions=[[p.xs,p.ys] for p in particles]
    return particlePositions,time

Es=[0.2,2,20,200]
Ss=[5]
Ns=[200]
Ms=[0.001,0.01,0.1,1,10]
Ts=[20]
DTs=[1/80]
MVs=[5,10,30]
rVelss=[True]

totalNum=len(Es)*len(Ss)*len(Ms)*len(Ns)*len(Ts)*len(DTs)*len(MVs)*len(rVelss)

# Transforma segundos para o formato: x horas y minutos z segundos (ChatGPT)
def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}h {m}m {s}s"

cont=0
dt=0

print("Número total de simulações:",totalNum)

for E in Es:
    for S in Ss:
        for N in Ns:
            for M in Ms:
                for T in Ts:
                    for DT in DTs:
                        for rVels in rVelss:
                            for MV in MVs:
                                t0=time.time()
                                with open("sims.json") as fs: data=json.load(fs)
                                
                                key="E="+str(E)+"+"
                                key+="S="+str(S)+"+"
                                key+="N="+str(N)+"+"
                                key+="M="+str(M)+"+"
                                key+="T="+str(T)+"+"
                                key+="DT="+str(DT)+"+"
                                key+="rV="+str(rVels)+"+"
                                key+="MV="+str(MV)

                                percent=round((100*cont)/totalNum,4)
                                timeToFinish=dt*(totalNum-cont)
                                print(percent,"% / Time to finish:",format_time(timeToFinish),"key saved:",key)

                                try: values=data[key]
                                except:
                                    p,t=CalculateSimulation(T,DT,N,M,E,S,rVels,MV)
                                    data[key]=1
                                    with open("sims.json",'w') as fs: json.dump(data,fs)
                                    with open("data/"+key+".json",'w') as fs: json.dump({"data":[p,list(t)]},fs)

                                dt=time.time()-t0
                                cont+=1

