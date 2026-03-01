import arcade
import numpy as np
import random
from distanceGenerator import GenerateAllData
import json
import os
log=False

# ------------------------------------- Global variables ---------------------------------
WIDTH=800
HEIGHT=500
agentScale=1.5
dy=10*agentScale
dx=7*agentScale
numOfAgents=20
moveSpeed=170
rotationSpeed=5
debugBallSize=3
numberOfRays=3
raioDeSeparacaoAteRaios=1
maxRayAngle=np.deg2rad(80)
rayDistance=80
mapSize=400
Map=[
    [3,2,2,2],
    [3,2,3,0],
    [1,1,1,2],
    [1,1,2,0]
]
numSeps=10
target=[0,len(Map)-1]
leastX=20
mostx=90
deathTimer=0
maxDeathTimer=15
numDead=0
mutationChance=0.2
mutationSTD=0.3
newNeuronChance=0.1
newConnectionChance=0.5
saveCounter=0
saveCounterMax=1
dataDir="MNNs"
loadData=False
distanceToConsiderWinner=20
maxLayers=10
if os.path.exists("EvolutionLearning/"+dataDir+".json") and not loadData:
    print("Já existe um diretório com o nome especificado, tem certeza que deseja continuar?")
    input()

# ------------------------------------- Variable inicialization ---------------------------------

Rss=[]
lineObstacles=[]
agents=[]
rays=[[[[0,0],[0,0],[0,0]] for _ in range(numberOfRays*2+1)] for _ in range(numOfAgents)]
rayCastResults=[[[False,0] for _ in range(2*numberOfRays+1)] for _ in range(numOfAgents)]
NNs=[]

# ------------------------------------- Simple variable calculations ---------------------------------

mapCells=len(Map)
Map.reverse()
DX=(mostx-leastX)/(numberOfRays*2+1)
debugHeight=HEIGHT/2
# Agent body pre-calculations
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
# Map variables
xBounds=[
    (WIDTH-mapSize)/2,
    (WIDTH+mapSize)/2
]
yBounds=[
    (HEIGHT-mapSize)/2,
    (HEIGHT+mapSize)/2
]
# Children
have=round(numOfAgents/2)
children=[]
while have>=1:
    numChildren=have
    children.append(numChildren)
    have=round(have/2)
sobra=numOfAgents-sum(children)
for i in range(sobra): children.append(1)
for i in range(int(numOfAgents-len(children))): children.append(0)
children.reverse()

absoluteTarget=[
    target[0]*(mapSize/mapCells)-(mapSize/2)+(mapSize/(2*mapCells))+WIDTH/2,
    target[1]*(mapSize/mapCells)-(mapSize/2)+(mapSize/(2*mapCells))+HEIGHT/2
]
# ------------------------------------- Functions ---------------------------------

def rand(): return random.randint(-300,300)/100

def GenerateNNs():
    global NNs,Rss
    for _ in range(numOfAgents):
        Neurons=[[] for _ in range(maxLayers)]
        Neurons[0]=[[0,[],3] for _ in range(numberOfRays*2+1)]
        Neurons[maxLayers-1]=[[random.randint(-100,100)/100,[[0,i,random.randint(-100,100)/100] for i in range(numberOfRays*2+1)],3] for _ in range(2)]
        NNs.append(Neurons)
    Rss=[[0,0] for _ in range(numOfAgents)]


def Sigmoid(vector):
    return (2/(1+np.exp(-vector)))-1

def GetActivation(indexOfAgent,i,j):
    global NNs
    Neurons=NNs[indexOfAgent]
    if Neurons[i][j][2]>2:
        activation=Neurons[i][j][0]
        for con in Neurons[i][j][1]:
            activation+=GetActivation(indexOfAgent,con[0],con[1])*con[2]
        activation=Sigmoid(activation)
        NNs[indexOfAgent][i][j][2]=activation
        return activation
    else: return Neurons[i][j][2]

def CalculateNN(indexOfAgent,inputs):
    global NNs,Rss
    for i,inp in enumerate(inputs):
        NNs[indexOfAgent][0][i][2]=inp
    outputs=[]
    for j in range(2):
        outputs.append(GetActivation(indexOfAgent,maxLayers-1,j))
    Rss[indexOfAgent]=outputs
    return outputs

def GenerateNewNeuron(indexOfAgent):
    global NNs
    layersWithNeurons=[]
    for layerID in range(maxLayers):
        if layerID>0:
            if len(NNs[indexOfAgent][layerID])>0: layersWithNeurons.append(layerID)
    for _ in range(10):
        randomLayer=layersWithNeurons[random.randint(0,len(layersWithNeurons)-1)]
        randomNeuron=random.randint(0,len(NNs[indexOfAgent][randomLayer])-1)
        randomConnection=random.randint(0,len(NNs[indexOfAgent][randomLayer][randomNeuron][1])-1)
        con=NNs[indexOfAgent][randomLayer][randomNeuron][1][randomConnection]
        distance=randomLayer-con[0]
        if distance>1:
            newNeuronLayer=random.randint(con[0]+1,randomLayer-1)
            newNeuronIndex=len(NNs[indexOfAgent][newNeuronLayer])
            oldCon=[val for val in NNs[indexOfAgent][randomLayer][randomNeuron][1][randomConnection]]
            oldCon[2]=1 # ? -> Weight between new neuron and neuron on lesser layer
            NNs[indexOfAgent][newNeuronLayer].append([0,[oldCon],3]) # ? -> Bias os new neuron
            NNs[indexOfAgent][randomLayer][randomNeuron][1][randomConnection]=[newNeuronLayer,newNeuronIndex,con[2]] # Weight between new neuron and neuron from greater layer
            return

def GenerateNewConnection(indexOfAgent):
    global NNs
    layersWithNeurons=[]
    for layerID in range(maxLayers):
        if layerID>0:
            if len(NNs[indexOfAgent][layerID])>0: layersWithNeurons.append(layerID)
    for _ in range(10):
        randomLayer=layersWithNeurons[random.randint(0,len(layersWithNeurons)-1)]
        randomNeuron=random.randint(0,len(NNs[indexOfAgent][randomLayer])-1)
        previousLayersWithNeurons=layersWithNeurons[:layersWithNeurons.index(randomLayer)]
        previousLayersWithNeurons.append(0)
        randomPreviousLayer=previousLayersWithNeurons[random.randint(0,len(previousLayersWithNeurons)-1)]
        randomNeuronPair=random.randint(0,len(NNs[indexOfAgent][randomPreviousLayer])-1)
        conExists=False
        for existingCon in NNs[indexOfAgent][randomLayer][randomNeuron][1]:
            if existingCon[0]==randomPreviousLayer and existingCon[1]==randomNeuronPair:
                conExists=True
                break
        if not conExists:
            NNs[indexOfAgent][randomLayer][randomNeuron][1].append([randomPreviousLayer,randomNeuronPair,0])
            return 

def GenerateAgents():
    global agents
    agents=[[WIDTH/2-mapSize/2+mapSize/(2*mapCells),HEIGHT/2-mapSize/2+mapSize/(2*mapCells),0,0,np.deg2rad(90),[[0,0],[0,0],[0,0]],False,-1] for _ in range(numOfAgents)]

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
    global numDead,agents
    for i in range(numOfAgents):
        if not agents[i][6]:
            dead=False
            for lineObstacle in lineObstacles:
                agent=agents[i]
                x,y,result=RayCast([agent[5][0],agent[5][1]],lineObstacle)
                if result:
                    #arcade.draw_circle_filled(x,y,5,[0,255,0])
                    dead=True
                x,y,result=RayCast([agent[5][1],agent[5][2]],lineObstacle)
                if result:
                    #arcade.draw_circle_filled(x,y,5,[0,255,0])
                    dead=True
                x,y,result=RayCast([agent[5][2],agent[5][0]],lineObstacle)
                if result:
                    #arcade.draw_circle_filled(x,y,5,[0,255,0])
                    dead=True
            if dead:
                numDead+=1
                agents[i][7]=GetDistance(agents[i][0],agents[i][1])

            agents[i][6]=dead


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
    if agent[6]: color=[255,0,0]
    else: color=[255,255,255]
    arcade.draw_line(agent[5][0][0],agent[5][0][1],agent[5][1][0],agent[5][1][1],color)
    arcade.draw_line(agent[5][1][0],agent[5][1][1],agent[5][2][0],agent[5][2][1],color)
    arcade.draw_line(agent[5][2][0],agent[5][2][1],agent[5][0][0],agent[5][0][1],color)

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
                #if result==True: arcade.draw_circle_filled(x,y,debugBallSize,[255,0,0])
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

def GetClosestPoint(x,y):
    quadrant=[(x-xBounds[0])//(mapSize/mapCells),(y-yBounds[0])//(mapSize/mapCells)]
    remain=[(x-xBounds[0])%(mapSize/mapCells),(y-yBounds[0])%(mapSize/mapCells)]
    miniCell=[remain[0]//((mapSize/mapCells)/numSeps),remain[1]//((mapSize/mapCells)/numSeps)]
    I=int(quadrant[0])
    J=int(quadrant[1])
    i=int(miniCell[0])
    j=int(miniCell[1])
    return I,J,i,j

def GetDistance(x,y):
    I,J,i,j=GetClosestPoint(x,y)
    return miniCellsDistances[I][J][i][j]

def Lerp(i,p1=[0,1,0],p2=[1,0,0]):
    r=max(min(p1[0]*(1-i)+p2[0]*i,255),0)
    g=max(min(p1[1]*(1-i)+p2[1]*i,255),0)
    b=max(min(p1[1]*(1-i)+p2[1]*i,255),0)
    return [r,g,b]

def MutateMatrix(matrix):
    mask=np.random.random(matrix.shape)<mutationChance
    noise=np.random.normal(0,mutationSTD,size=matrix.shape)
    return matrix+(noise*mask)

def deepCopy(obj):
    if type(obj)==list:
        return [deepCopy(item) for item in obj]
    else: return obj   

def MutateAll(): 
    global NNs,log
    scores=[agent[7] for agent in agents]
    indexes=[i for i in range(numOfAgents)]
    indices=list(np.argsort(scores))
    indices.reverse()
    indexes=[indexes[i] for i in indices]
    scores=[scores[i] for i in indices]
    newNNs=[]
    if log: print("----------------------------------------------------------------------")
    if log: print("NNs",NNs)
    if log: print("Children:",children)
    for i in range(numOfAgents):
        numberOfChildren=children[i]
        if numberOfChildren>0:
            indexOfAgent=indexes[i]
            for _ in range(numberOfChildren):
                newNNs.append(deepCopy(NNs[indexOfAgent]))
    if log: print("Number of newNNs:",len(newNNs))
    if log: print("newNNs:",newNNs)
    NNs=newNNs
    if log: print("NNs:",NNs)
    for indexOfAgent in range(numOfAgents):
        if random.randint(0,100)/100<newNeuronChance:
            if log: print("  Generated new neuron")
            GenerateNewNeuron(indexOfAgent)
        if random.randint(0,100)/100<newConnectionChance:
            if log: print("  Generated new conection")
            GenerateNewConnection(indexOfAgent)
        if log: print("  Agent["+str(indexOfAgent)+"] new NN after newNeuron/Con:",NNs[indexOfAgent])
        for layerID in range(len(NNs[indexOfAgent])):
            for neuronID in range(len(NNs[indexOfAgent][layerID])):
                if random.randint(0,100)/100<mutationChance:
                    NNs[indexOfAgent][layerID][neuronID][0]+=np.random.normal(0,mutationSTD)
                    if log: print("    Changed bias")
                NNs[indexOfAgent][layerID][neuronID][2]=3
                for conID in range(len(NNs[indexOfAgent][layerID][neuronID][1])):
                    if random.randint(0,100)/100<mutationChance:
                        if log: print("      Changed weight")
                        NNs[indexOfAgent][layerID][neuronID][1][conID][2]+=np.random.normal(0,mutationSTD)
        if log: print("Agent["+str(indexOfAgent)+"] new NN after mutation:",NNs[indexOfAgent])

def ConvertToList(npArray):
    convertedList=[]
    for item in npArray:
        try:
            float(item)
            convertedList.append(item)
        except:
            convertedList.append(ConvertToList(item))
    return convertedList

def Save():
    '''listWss=ConvertToList(Wss)
    listBss=ConvertToList(Bss)
    dic={"Wss":listWss,"Bss":listBss}
    with open("EvolutionLearning/"+dataDir+".json",'w') as fs: json.dump(dic,fs)'''

def Load():
    '''global Wss,Bss
    with open("EvolutionLearning/"+dataDir+".json") as fs: dic=json.load(fs)
    Wss=[[np.array(W) for W in Ws] for Ws in dic["Wss"]]
    Bss=[[np.array(B) for B in Bs] for Bs in dic["Bss"]]'''


# ------------------------------------- Inicial Function Calls ---------------------------------
GenerateNNs()
GenerateAgents()
miniCells,miniCellsDistances,maximum=GenerateAllData(WIDTH,HEIGHT,mapSize,Map,numSeps,target)
if loadData: Load()

# ------------------------------------- Array construction ---------------------------------

# Map generation
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

for i in range(len(lineObstacles)):
    lineObstacles[i][0][0]=lineObstacles[i][0][0]+WIDTH/2
    lineObstacles[i][0][1]=lineObstacles[i][0][1]+HEIGHT/2
    lineObstacles[i][1][0]=lineObstacles[i][1][0]+WIDTH/2
    lineObstacles[i][1][1]=lineObstacles[i][1][1]+HEIGHT/2



xsPositions=[leastX+i*DX for i in range(2*numberOfRays+1)]

# ------------------------------------- Arcade Class ---------------------------------

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
        DoRayCasts()
        inputs=[]
        for j in range(2*numberOfRays+1):
            rr=rayCastResults[0][j]
            percent=rr[1]/rayDistance
            inputs.append(percent)
            color=Lerp(percent,[255,255,255],[0,0,0])
            arcade.draw_circle_filled(xsPositions[j],debugHeight,5,color)
        for i in range(numOfAgents):
            inputs=[]
            for j in range(2*numberOfRays+1):
                rr=rayCastResults[i][j]
                percent=rr[1]/rayDistance
                inputs.append(percent)
            activations=CalculateNN(i,inputs)
        for k,activation in enumerate(activations):
            color=Lerp((activation+1)/2,[0,255,0],[255,0,0])
            arcade.draw_circle_filled(xsPositions[k],debugHeight-15,5,color)

    def Reset(self):
        global deathTimer,numDead,agents,saveCounter
        deathTimer=0
        for i,agent in enumerate(agents):
            if agent[7]==-1:
                agents[i][7]=GetDistance(agent[0],agent[1])
        MutateAll()
        GenerateAgents()
        numDead=0
        saveCounter+=1
        if saveCounter>=saveCounterMax:
            Save()
            saveCounter=0
    
    def on_update(self, delta_time):
        global deathTimer,agents,numDead,NNs
        for i,agent in enumerate(agents):
            if not agent[6]:
                moveCommand=Rss[i]
                for layerID in range(len(NNs[i])):
                    for neuronID in range(len(NNs[i][layerID])):
                        NNs[i][layerID][neuronID][2]=3
                agent[2]=moveCommand[0]
                agent[3]=moveCommand[1]
        for agent in agents:
            if not agent[6]:
                agent[4]+=agent[2]*delta_time*rotationSpeed
                agent[0]+=np.cos(agent[4])*agent[3]*moveSpeed*delta_time
                agent[1]+=np.sin(agent[4])*agent[3]*moveSpeed*delta_time
        for i in range(numOfAgents):
            CalculatePointsPosition(i)
            RaycastGenerators(i)
        CheckAgentCollision()
        deathTimer+=delta_time
        if deathTimer>=maxDeathTimer: self.Reset()
        if numDead>=numOfAgents: self.Reset()

        for i in range(numOfAgents):
            agent=agents[i]
            if not agent[6]:
                distanceToGoal=np.sqrt(((agent[0]-absoluteTarget[0])**2)+((agent[1]-absoluteTarget[1])**2))
                if distanceToGoal<distanceToConsiderWinner:
                    agents[i][6]=True
                    numDead+=1
    
    def on_key_press(self, symbol, modifiers):
        '''if symbol==arcade.key.W: self.moveCommand[1]+=1
        if symbol==arcade.key.A: self.moveCommand[0]+=1
        if symbol==arcade.key.S: self.moveCommand[1]-=1
        if symbol==arcade.key.D: self.moveCommand[0]-=1
        return super().on_key_press(symbol, modifiers)'''
        pass

    def on_key_release(self, symbol, modifiers):
        '''if symbol==arcade.key.W: self.moveCommand[1]-=1
        if symbol==arcade.key.A: self.moveCommand[0]-=1
        if symbol==arcade.key.S: self.moveCommand[1]+=1
        if symbol==arcade.key.D: self.moveCommand[0]+=1
        return super().on_key_release(symbol, modifiers)'''
        pass


if __name__ == "__main__":
    window = MySimulation()
    arcade.run()