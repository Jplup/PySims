import numpy as np
import matplotlib.pyplot as plt
import random
from distanceGenerator import GenerateAllData

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
numSeps=7

Map=[
    [3,2,2,2],
    [3,2,3,0],
    [1,1,1,2],
    [1,1,2,0]
]
mapCells=len(Map)
print("Map cells:",mapCells)
Map.reverse()

target=[0,len(Map)-1]
start=[0,0]

absoluteTarget=[
    target[0]*(mapSize/mapCells)-(mapSize/2)+(mapSize/(2*mapCells))+WIDTH/2,
    target[1]*(mapSize/mapCells)-(mapSize/2)+(mapSize/(2*mapCells))+HEIGHT/2
]
absoluteStart=[
    start[0]*(mapSize/mapCells)-(mapSize/2)+(mapSize/(2*mapCells))+WIDTH/2,
    start[1]*(mapSize/mapCells)-(mapSize/2)+(mapSize/(2*mapCells))+HEIGHT/2
]

lineObstacles=[]

def deepCopy(lista:list,nullify=False):
    newList=[]
    for item in lista:
        if type(item)==list:
            newList.append(deepCopy(item,nullify))
        else:
            if nullify: newList.append(-1)
            else: newList.append(item)
    return newList

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
                deepCopy(corner),
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

miniCells,miniCellsDistances,maximum=GenerateAllData(WIDTH,HEIGHT,mapSize,Map,numSeps,target)

def Lerp(i,p1=[0,1,0],p2=[1,0,0]):
    r=max(min(p1[0]*(1-i)+p2[0]*i,1),0)
    g=max(min(p1[1]*(1-i)+p2[1]*i,1),0)
    return [r,g,0]

def plotDistanceIndicator(I,J,i,j):
    center=miniCells[I][J][i][j]
    distance=miniCellsDistances[I][J][i][j]
    color=Lerp(distance/maximum)
    plt.scatter(center[0],center[1],c=color)


for I in range(mapCells):
    for J in range(mapCells):
        for i in range(numSeps):
            for j in range(numSeps):
                #plotWallsIndicator(I,J,i,j)
                plotDistanceIndicator(I,J,i,j)
                pass

xBounds=[
    (WIDTH-mapSize)/2,
    (WIDTH+mapSize)/2
]
yBounds=[
    (HEIGHT-mapSize)/2,
    (HEIGHT+mapSize)/2
]

def GetClosestPoint(x,y):
    quadrant=[(x-xBounds[0])//(mapSize/mapCells),(y-yBounds[0])//(mapSize/mapCells)]
    remain=[(x-xBounds[0])%(mapSize/mapCells),(y-yBounds[0])%(mapSize/mapCells)]
    miniCell=[remain[0]//((mapSize/mapCells)/numSeps),remain[1]//((mapSize/mapCells)/numSeps)]
    #print("Quadrant:",quadrant,"/ remain:",remain,"minicell:",miniCell)
    I=int(quadrant[0])
    J=int(quadrant[1])
    i=int(miniCell[0])
    j=int(miniCell[1])
    miniCellPosition=miniCells[I][J][i][j]
    return miniCellPosition,[I,J,i,j],np.sqrt(((x-miniCellPosition[0])**2)+((y-miniCellPosition[1])**2))
    
colors=['r','g','b','k']
colors=[]
for i in range(len(colors)):
    rx=random.randint(int(xBounds[0]+mapSize/10),int(xBounds[1]-mapSize/10))
    ry=random.randint(int(yBounds[0]+mapSize/10),int(yBounds[1]-mapSize/10))
    print("rx:",rx,"ry:",ry,"color:",colors[i])
    position,indices,dist=GetClosestPoint(rx,ry)
    print("Closest position:",position,"indices:",indices,"distance:",dist)
    distance=miniCellsDistances[indices[0]][indices[1]][indices[2]][indices[3]]
    plt.scatter(position[0],position[1],c=Lerp(distance/maximum))
    plt.scatter(rx,ry,c=colors[i])

for lineObstacle in lineObstacles:
    xs=[lineObstacle[0][0],lineObstacle[1][0]]
    ys=[lineObstacle[0][1],lineObstacle[1][1]]
    plt.plot(xs,ys,c='k')
plt.axis("equal")
plt.show()