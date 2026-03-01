import arcade
import numpy as np
import random

WIDTH = 800
HEIGHT = 500
agentScale=1.5
dy=10*agentScale
dx=7*agentScale
numOfAgents=1
moveSpeed=170
rotationSpeed=5
debugBallSize=3
numberOfRays=3
raioDeSeparacaoAteRaios=5
maxRayAngle=np.deg2rad(80)
rayDistance=80
mapSize=400

points=[
    [-dx,-dy],
    [0,dy],
    [dx,-dy]
]

distances=[
    np.sqrt(dx**2+dy**2),
    np.sqrt(dy**2),
    np.sqrt(dx**2+dy**2)
]

angles=[
    np.arctan2(-dy,-dx)-np.deg2rad(90),
    0,
    np.arctan2(-dy,dx)-np.deg2rad(90)
]

def rand(): return random.randint(-300,300)/100

Wss=[]
Bss=[]
layers=[2*numberOfRays+1,4,2]
def GenerateNNs():
    global Wss,Bss
    Wss=[]
    Bss=[]
    for _ in range(numOfAgents):
        Ws=[]
        Bs=[]
        for i in range(len(layers)-1):
            Wi=np.array([[rand() for _ in range(layers[i+1])] for _ in range(layers[i])])
            Ws.append(Wi)
            Bi=np.transpose(np.array([rand() for _ in range(layers[i+1])]))
            Bs.append(Bi)
        Wss.append(Ws)
        Bss.append(Bs)
GenerateNNs()

def Sigmoid(vector):
    return (2/(1+np.exp(-vector)))-1

def CalculateNN(I,indexOfAgent):
    I0=np.array(I)
    lastI=I0
    for i in range(len(layers)-1):
        Ii1=(lastI@Wss[indexOfAgent][i])+Bss[indexOfAgent][i]
        lastI=Sigmoid(Ii1)
    return lastI

rays=[[[[0,0],[0,0],[0,0]] for _ in range(numberOfRays*2+1)] for _ in range(numOfAgents)]

Map=[
    [3,2,2,2],
    [3,2,3,0],
    [1,1,1,2],
    [1,1,2,0]
]
mapCells=len(Map)
print("Map cells:",mapCells)
Map.reverse()

lineObstacles=[]

for i in range(mapCells):
    for j in range(mapCells):
        corner=[(mapSize/mapCells)*i-(mapSize/2),(mapSize/mapCells)*j-(mapSize/2)]
        if Map[j][i]==1 or Map[j][i]==3:
            lineObstacles.append([corner,[corner[0],corner[1]+(mapSize/mapCells)]])
        if Map[j][i]==2 or Map[j][i]==3:
            lineObstacles.append([
                [corner[0],corner[1]+(mapSize/mapCells)],
                [corner[0]+(mapSize/mapCells),corner[1]+(mapSize/mapCells)]
            ])
        if j==0:
            lineObstacles.append([
                corner.copy(),
                [corner[0]+(mapSize/mapCells),corner[1]]
            ])
        if i==(mapCells-1):
            lineObstacles.append([
                [corner[0]+(mapSize/mapCells),corner[1]],
                [corner[0]+(mapSize/mapCells),corner[1]+(mapSize/mapCells)]
            ])

#print("Line Obstacles:",lineObstacles)

for i in range(len(lineObstacles)):
    #print("------------- i =",i,"------------------------")
    #print("Old:",lineObstacles[i])
    lineObstacles[i][0][0]=lineObstacles[i][0][0]+WIDTH/2
    lineObstacles[i][0][1]=lineObstacles[i][0][1]+HEIGHT/2
    lineObstacles[i][1][0]=lineObstacles[i][1][0]+WIDTH/2
    lineObstacles[i][1][1]=lineObstacles[i][1][1]+HEIGHT/2
    #print("New:",lineObstacles[i])

#print("Line Obstacles:",lineObstacles)

agents=[]
def GenerateAgents():
    global agents
    agents=[[WIDTH/2-mapSize/2+mapSize/(2*mapCells),HEIGHT/2-mapSize/2+mapSize/(2*mapCells),0,0,np.deg2rad(90),[[0,0],[0,0],[0,0]]] for _ in range(numOfAgents)]
GenerateAgents()

def RayCast(line1,line2):
    # Extrai pontos
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    # Calcula denominador (produto vetorial)
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return 0, 0, False  # Segmentos paralelos ou colineares

    # Parâmetros t para line1 e u para line2
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    # Verifica se a interseção está dentro dos segmentos (0 <= t <= 1 e 0 <= u <= 1)
    if 0 <= t <= 1 and 0 <= u <= 1:
        # Ponto de interseção
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return x, y, True
    else:
        return 0, 0, False
    
def RaycastGenerators(indexOfAgent):
    B=[
        dy*np.cos(agents[indexOfAgent][4])+agents[indexOfAgent][0],
        dy*np.sin(agents[indexOfAgent][4])+agents[indexOfAgent][1]
    ]
    for i in range(2*numberOfRays+1):
        beta=(maxRayAngle/numberOfRays)*i-maxRayAngle
        pi=[
            raioDeSeparacaoAteRaios*np.cos(beta+agents[indexOfAgent][4])+B[0],
            raioDeSeparacaoAteRaios*np.sin(beta+agents[indexOfAgent][4])+B[1]
        ]
        pf=[
            (rayDistance+raioDeSeparacaoAteRaios)*np.cos(beta+agents[indexOfAgent][4])+B[0],
            (rayDistance+raioDeSeparacaoAteRaios)*np.sin(beta+agents[indexOfAgent][4])+B[1]
        ]
        rays[indexOfAgent][i][0]=pi
        rays[indexOfAgent][i][1]=pf

def CheckAgentCollision():
    deads=[]
    for i in range(numOfAgents):
        dead=False
        for lineObstacle in lineObstacles:
            agent=agents[i]
            x,y,result=RayCast([agent[5][0],agent[5][1]],lineObstacle)
            if result:
                arcade.draw_circle_filled(x,y,5,[0,255,0])
                dead=True
            x,y,result=RayCast([agent[5][1],agent[5][2]],lineObstacle)
            if result:
                arcade.draw_circle_filled(x,y,5,[0,255,0])
                dead=True
            x,y,result=RayCast([agent[5][2],agent[5][0]],lineObstacle)
            if result:
                arcade.draw_circle_filled(x,y,5,[0,255,0])
                dead=True
        deads.append(dead)
    return deads


def CalculatePointsPosition(indexOfAgent):
    agent=agents[indexOfAgent]
    for i in range(3):
        newPosition=[
                np.cos(angles[i]+agent[4])*distances[i]+agent[0],
                np.sin(angles[i]+agent[4])*distances[i]+agent[1]
        ]
        agents[indexOfAgent][5][i]=newPosition

def DrawAgent(index):
    agent=agents[index]
    arcade.draw_line(agent[5][0][0],agent[5][0][1],agent[5][1][0],agent[5][1][1],[255,255,255])
    arcade.draw_line(agent[5][1][0],agent[5][1][1],agent[5][2][0],agent[5][2][1],[255,255,255])
    arcade.draw_line(agent[5][2][0],agent[5][2][1],agent[5][0][0],agent[5][0][1],[255,255,255])

rayCastResults=[[[False,0] for _ in range(2*numberOfRays+1)] for _ in range(numOfAgents)]

def DoRayCasts():
    for i in range(numOfAgents):
        for j in range(2*numberOfRays+1):
            colisions=[]
            for lineObstacle in lineObstacles:
                ray=rays[i][j]
                x,y,result=RayCast(ray,lineObstacle)
                rayStartPoint=rays[i][j][0]
                distance=np.sqrt(((rayStartPoint[0]-x)**2)+((rayStartPoint[1]-y)**2))
                colisions.append([x,y,result,distance])
                if result==True: arcade.draw_circle_filled(x,y,debugBallSize,[255,0,0])
            least=9999999
            leastK=-1
            for k,colision in enumerate(colisions):
                if colision[2]:
                    if colision[3]<least:
                        least=colision[3]
                        leastK=k
            if leastK==-1:
                rayCastResults[i][j]=[False,rayDistance]
            else:
                rayCastResults[i][j]=[True,least]

leastX=20
mostx=90
DX=(mostx-leastX)/(numberOfRays*2+1)
xsPositions=[leastX+i*DX for i in range(2*numberOfRays+1)]
debugHeight=HEIGHT/2
print("xsPositions:",xsPositions)
def Lerp(i,p1=[0,1,0],p2=[1,0,0]):
    r=max(min(p1[0]*(1-i)+p2[0]*i,255),0)
    g=max(min(p1[1]*(1-i)+p2[1]*i,255),0)
    b=max(min(p1[1]*(1-i)+p2[1]*i,255),0)
    return [r,g,b]

deathTimer=0
maxDeathTimer=5

class MySimulation(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Evo - Arcade")
        self.moveCommand=[0,0]
        
    def on_draw(self):
        self.clear()
        for lineObstacle in lineObstacles:
            arcade.draw_line(lineObstacle[0][0],lineObstacle[0][1],lineObstacle[1][0],lineObstacle[1][1],[0,255,255])
        for i in range(numOfAgents):
            DrawAgent(i)
            for rayIndex in range(2*numberOfRays+1):
                ray=rays[i][rayIndex]
                arcade.draw_line(ray[0][0],ray[0][1],ray[1][0],ray[1][1],[0,255,0])
        DoRayCasts()
        inputs=[]
        for j in range(2*numberOfRays+1):
            rr=rayCastResults[0][j]
            percent=rr[1]/rayDistance
            inputs.append(percent)
            color=Lerp(percent,[255,255,255],[0,0,0])
            arcade.draw_circle_filled(xsPositions[j],debugHeight,5,color)
        activations=CalculateNN(inputs,0)
        for k,activation in enumerate(activations):
            color=Lerp((activation+1)/2,[0,255,0],[255,0,0])
            arcade.draw_circle_filled(xsPositions[k],debugHeight-15,5,color)
        self.moveCommand[1]=activations[0]
        self.moveCommand[0]=activations[1]
        '''if activations[0]>0.3: self.moveCommand[1]=1
        else:
            if activations[0]<-0.3: self.moveCommand[1]=-1
            else: self.moveCommand[1]=0
        if activations[1]>0.3: self.moveCommand[0]=1
        else:
            if activations[1]<-0.3: self.moveCommand[0]=-1
            else: self.moveCommand[0]=0'''
        deads=CheckAgentCollision()

        if deads[0]: self.Reset()

    def Reset(self):
        global deathTimer
        deathTimer=0
        GenerateAgents()
        GenerateNNs()
    
    def on_update(self, delta_time):
        global deathTimer
        for agent in agents:
            agent[2]=self.moveCommand[0]
            agent[3]=self.moveCommand[1]
        for agent in agents:
            agent[4]+=agent[2]*delta_time*rotationSpeed
            agent[0]+=np.cos(agent[4])*agent[3]*moveSpeed*delta_time
            agent[1]+=np.sin(agent[4])*agent[3]*moveSpeed*delta_time
        for i in range(numOfAgents):
            CalculatePointsPosition(i)
            RaycastGenerators(i)
        deathTimer+=delta_time
        if deathTimer>=maxDeathTimer: self.Reset()     
    
    def on_key_press(self, symbol, modifiers):
        if symbol==arcade.key.W: self.moveCommand[1]+=1
        if symbol==arcade.key.A: self.moveCommand[0]+=1
        if symbol==arcade.key.S: self.moveCommand[1]-=1
        if symbol==arcade.key.D: self.moveCommand[0]-=1
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if symbol==arcade.key.W: self.moveCommand[1]-=1
        if symbol==arcade.key.A: self.moveCommand[0]-=1
        if symbol==arcade.key.S: self.moveCommand[1]+=1
        if symbol==arcade.key.D: self.moveCommand[0]+=1
        return super().on_key_release(symbol, modifiers)


if __name__ == "__main__":
    window = MySimulation()
    arcade.run()