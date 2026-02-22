import numpy as np
import matplotlib.pyplot as plt
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

count=0
colors=['r','g','b','k','y','m']
miniCellSize=(mapSize/mapCells)/numSeps
mcs=miniCellSize
miniCells=[]
for I in range(mapCells):
    miniCellsXs=[]
    for J in range(mapCells):
        centerOfCell=[
            (mapSize/mapCells)*(I+0.5)-(mapSize/2)+WIDTH/2,
            (mapSize/mapCells)*(J+0.5)-(mapSize/2)+HEIGHT/2
        ]
        miniCellsYs=[]
        for i in range(numSeps):
            miniCellsxs=[]
            for j in range(numSeps):
                littleQuad=[
                    centerOfCell[0]+mcs*i-(mapSize/mapCells)/2+mcs/2,
                    centerOfCell[1]+mcs*j-(mapSize/mapCells)/2+mcs/2
                ]
                miniCellsxs.append(deepCopy(littleQuad))
            miniCellsYs.append(deepCopy(miniCellsxs))
        miniCellsXs.append(deepCopy(miniCellsYs))
        count+=1
        if count>=len(colors): count=0
    miniCells.append(deepCopy(miniCellsXs))

def append(lista:list,value):
    if not value in lista: lista.append(value)

miniCellsWalls=deepCopy(miniCells)
for I in range(mapCells):
    for J in range(mapCells):
        for i in range(numSeps):
            for j in range(numSeps):
                # Bordas dos quadrantes: tem que checar parede
                if i==0 or i==numSeps-1 or j==0 or j==numSeps-1:
                    miniCellsWalls[I][J][i][j]=[]
                    for di in [-1,1]:
                        for dj in [-1,1]:
                            ni=i+di
                            nj=j+dj
                            # Se isso for verdade, a minicélula vizinha está dentro do mesmo
                            #   quadrante da de estudo, ou seja, com certeza não tem parede
                            #   entre elas, pois não tem parede dentro de quadrantes
                            if ni>=0 and ni<=numSeps-1 and nj>=0 and nj<=numSeps-1: pass
                            else:
                                # Vizinho está em um quadrante da esquerda
                                if ni<0:
                                    # Vizinho está no quadrante inferior esquerdo
                                    if nj<0:
                                        # Se existe o quadrante:
                                        if I-1>=0 and J-1>=0:
                                            # Se o quadrante inferior esquerdo tem parede encima
                                            #   ou o embaixo tem parede na esquerda:
                                            if Map[J-1][I-1]==2 or Map[J-1][I-1]==3 or Map[J-1][I]==1 or Map[J-1][I]==3:
                                                append(miniCellsWalls[I][J][i][j],6)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],6)
                                    # Vizinho está no quadrante superior esquerdo
                                    elif nj==numSeps:
                                        # Se existe o quadrante:
                                        if I-1>=0 and J+1<mapCells:
                                            # Se o quadrante da esquerda tem parede encima
                                            #   ou o de cima tem parede na esquerda:
                                            if Map[J][I-1]==2 or Map[J][I-1]==3 or Map[J+1][I]==1 or Map[J+1][I]==3:
                                                append(miniCellsWalls[I][J][i][j],1)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],1)
                                    # Vizinho está no quadrante da esquerda
                                    else:
                                        # Se o quadrante da esquerda existe:
                                        if I-1>=0:
                                            # Tem parede
                                            if 1==Map[J][I] or 3==Map[J][I]:
                                                append(miniCellsWalls[I][J][i][j],4)
                                                append(miniCellsWalls[I][J][i][j],1)
                                                append(miniCellsWalls[I][J][i][j],6)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],4)
                                            append(miniCellsWalls[I][J][i][j],1)
                                            append(miniCellsWalls[I][J][i][j],6)
                                # Vizinho está em um quadrante da direita
                                elif ni==numSeps:
                                    # Vizinho está no quadrante inferior direito
                                    if nj<0:
                                        # Se existe o quadrante:
                                        if I+1<mapCells and J-1>=0:
                                            # Se o quadrante inferior direito tem parede na 
                                            #   esquerda ou em cima:
                                            if not Map[J-1][I+1]==0:
                                                append(miniCellsWalls[I][J][i][j],8)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],8)
                                    # Vizinho está no quadrante superior direito
                                    elif nj==numSeps:
                                        # Se existe o quadrante:
                                        if I+1<mapCells and J+1<mapCells:
                                            # Se o quadrante direito tem parede encima 
                                            #   ou o quadrante superior direito tem na esquerda:
                                            if Map[J][I+1]==2 or Map[J][I+1]==3 or Map[J+1][I+1]==1 or Map[J+1][I+1]==3:
                                                append(miniCellsWalls[I][J][i][j],3)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],3)
                                    # Vizinho está no quadrante da direita
                                    else:
                                        # Se o quadrante da direita existe:
                                        if I+1<mapCells:
                                            # Tem parede
                                            if 1==Map[J][I+1] or 3==Map[J][I+1]:
                                                append(miniCellsWalls[I][J][i][j],5)
                                                append(miniCellsWalls[I][J][i][j],3)
                                                append(miniCellsWalls[I][J][i][j],8)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],5)
                                            append(miniCellsWalls[I][J][i][j],3)
                                            append(miniCellsWalls[I][J][i][j],8)
                                # Vizinho está encima ou embaixo:
                                else:
                                    # Vizinho está no quadrante inferior
                                    if nj<0:
                                        # Se o quadrante inferior existe:
                                        if J-1>=0:
                                            # Tem parede
                                            if 2==Map[J-1][I] or 3==Map[J-1][I]:
                                                append(miniCellsWalls[I][J][i][j],7)
                                                append(miniCellsWalls[I][J][i][j],6)
                                                append(miniCellsWalls[I][J][i][j],8)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],7)
                                            append(miniCellsWalls[I][J][i][j],6)
                                            append(miniCellsWalls[I][J][i][j],8)
                                    # Vizinho está no quadrante superior
                                    elif nj==numSeps:
                                        # Se o quadrante superior existe:
                                        if J+1<mapCells:
                                            # Tem parede
                                            if 2==Map[J][I] or 3==Map[J][I]:
                                                append(miniCellsWalls[I][J][i][j],2)
                                                append(miniCellsWalls[I][J][i][j],1)
                                                append(miniCellsWalls[I][J][i][j],3)
                                        # Se não existir, tem a parede com certeza:
                                        else:
                                            append(miniCellsWalls[I][J][i][j],2)
                                            append(miniCellsWalls[I][J][i][j],1)
                                            append(miniCellsWalls[I][J][i][j],3)

miniCellsDistances=[[[[-1 for _ in range(numSeps)] for _ in range(numSeps)] for _ in range(mapCells)] for _ in range(mapCells)]
cellsToUseToUpdate=[]
if (numSeps%2)==0:
    middle=int(numSeps/2)-1
    for dx,dy in zip([0,0,1,1],[0,1,0,1]):
        miniCellsDistances[target[0]][target[1]][middle+dx][middle+dy]=0
        cellsToUseToUpdate.append([target[0],target[1],middle+dx,middle+dy])
else:
    middle=int(numSeps/2)
    miniCellsDistances[target[0]][target[1]][middle][middle]=0
    cellsToUseToUpdate.append([target[0],target[1],middle,middle])

#print("Cells to update:",cellsToUseToUpdate)
while len(cellsToUseToUpdate)>0:
    #print("------------------------Entrou no while--------------------------")
    staggeredList=[]
    #print("Staggerd list:",staggeredList)
    for cell in cellsToUseToUpdate:
        #print("  cell:",cell)
        I,J,i,j=cell
        #print("  I:",I,"J:",J,"i:",i,"j:",j)
        currentDistance=miniCellsDistances[I][J][i][j]
        #print("  current distance:",currentDistance)
        # Update neibours
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx==0 and dy==0: pass
                else:
                    neibour=[I,J,i+dx,j+dy]
                    #print("    ----neibour---- =",neibour)
                    # Se o vizinho está pra fora da célula pro lado esquerdo:
                    if i+dx<0:
                        #print("    neibours x is not in bounds (<0)")
                        # e tem células para a esquerda:
                        if I-1>=0:
                            # O index em x vai pro outro lado (dá a volta)
                            neibour[2]=numSeps-1
                            neibour[0]-=1
                            # Se o vizinho está na célula inferior esquerda
                            if j+dy<0:
                                # e existe essa célula:
                                if J-1>=0:
                                    # O index em y vai pro outro lado (dá a volta)
                                    neibour[3]=numSeps-1
                                    neibour[1]-=1
                                    # Checa se tem parede indo nessa direção:
                                    if 6 in miniCellsWalls[I][J][i][j]:
                                        # Tem parede, não pode fazer o update
                                        pass
                                    else:
                                        if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                            miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+np.sqrt(2)
                                            staggeredList.append(deepCopy(neibour))
                                else: pass # Não existe esse vizinho
                            # Se o vizinho está na célula superior esquerda
                            elif j+dy>=numSeps:
                                # e existe essa célula:
                                if J+1<mapCells:
                                    # O index em y vai pro outro lado (dá a volta)
                                    neibour[3]=0
                                    neibour[1]+=1
                                    # Checa se tem parede indo nessa direção:
                                    if 1 in miniCellsWalls[I][J][i][j]:
                                        # Tem parede, não pode fazer o update
                                        pass
                                    else:
                                        if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                            miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+np.sqrt(2)
                                            staggeredList.append(deepCopy(neibour))
                                else: pass # Não existe esse vizinho
                            # Se o vizinho está na célula esquerda
                            else:
                                # O check de se tem a célula na esquerda já foi feito antes
                                # Checa se tem parede indo nessa direção:
                                if 4 in miniCellsWalls[I][J][i][j]:
                                    # Tem parede, não pode fazer o update
                                    pass
                                else:
                                    if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                        miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+1
                                        staggeredList.append(deepCopy(neibour))
                        else: pass # Não existe esse vizinho
                    # Se o vizinho está para fora da célula, pro lado direito
                    elif i+dx>=numSeps:
                        #print("    neibours x is not in bounds (>size)")
                        # e tem células para a direita:
                        if I+1<mapCells:
                            # O index em x vai pro outro lado (dá a volta)
                            neibour[2]=0
                            neibour[0]+=1
                            # Se o vizinho está na célula inferior direita
                            if j+dy<0:
                                # e existe essa célula:
                                if J-1>=0:
                                    # O index em y vai pro outro lado (dá a volta)
                                    neibour[3]=numSeps-1
                                    neibour[1]-=1
                                    # Checa se tem parede indo nessa direção:
                                    if 8 in miniCellsWalls[I][J][i][j]:
                                        # Tem parede, não pode fazer o update
                                        pass
                                    else:
                                        if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                            miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+np.sqrt(2)
                                            staggeredList.append(deepCopy(neibour))
                                else: pass # Não existe esse vizinho
                            # Se o vizinho está na célula superior direita
                            elif j+dy>=numSeps:
                                # e existe essa célula:
                                if J+1<mapCells:
                                    # O index em y vai pro outro lado (dá a volta)
                                    neibour[3]=0
                                    neibour[1]+=1
                                    # Checa se tem parede indo nessa direção:
                                    if 3 in miniCellsWalls[I][J][i][j]:
                                        # Tem parede, não pode fazer o update
                                        pass
                                    else:
                                        if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                            miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+np.sqrt(2)
                                            staggeredList.append(deepCopy(neibour))
                                else: pass # Não existe esse vizinho
                            # Se o vizinho está na célula direita
                            else:
                                # O check de se tem a célula na direita já foi feito antes
                                # Checa se tem parede indo nessa direção:
                                if 5 in miniCellsWalls[I][J][i][j]:
                                    # Tem parede, não pode fazer o update
                                    pass
                                else:
                                    if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                        miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+1
                                        staggeredList.append(deepCopy(neibour))
                        else: pass # Não existe esse vizinho
                    # Se o vizinho não está para a esquerda nem direita da célula de estudo
                    else:
                        #print("    neibours x is in bounds")
                        # Se o vizinho está na célula inferior
                        if j+dy<0:
                            #print("    neibours y is not in bounds (<0)")
                            # e existe essa célula:
                            if J-1>=0:
                                # O index em y vai pro outro lado (dá a volta)
                                neibour[3]=numSeps-1
                                neibour[1]-=1
                                # Checa se tem parede indo nessa direção:
                                if 7 in miniCellsWalls[I][J][i][j]:
                                    # Tem parede, não pode fazer o update
                                    pass
                                else:
                                    if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                        miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+1
                                        staggeredList.append(deepCopy(neibour))
                            else: pass # Não existe esse vizinho
                        # Se o vizinho está na célula superior
                        elif j+dy>=numSeps:
                            #print("    neibours y is not in bounds (>size)")
                            # e existe essa célula:
                            if J+1<mapCells:
                                # O index em y vai pro outro lado (dá a volta)
                                neibour[3]=0
                                neibour[1]+=1
                                # Checa se tem parede indo nessa direção:
                                if 2 in miniCellsWalls[I][J][i][j]:
                                    # Tem parede, não pode fazer o update
                                    pass
                                else:
                                    if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                        miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+1
                                        staggeredList.append(deepCopy(neibour))
                            else: pass # Não existe esse vizinho
                        # Se o vizinho está na mesma célula da de estudo: não tem parede com certeza
                        else:
                            #print("    neibours y is in bounds")
                            if abs(dx)+abs(dy)==2:
                                #print("    neibour is in diagonal")
                                if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                    #print("    neibour didnt have distance")
                                    miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+np.sqrt(2)
                                    #print("    neibours distance:",miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]])
                                    staggeredList.append(deepCopy(neibour))
                                    #print("    staggerd list:",staggeredList)
                            else:
                                #print("    neibour is orthogonal")
                                if miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]==-1:
                                    #print("    neibour didnt have distance")
                                    miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]]=currentDistance+1
                                    #print("    neibours distance:",miniCellsDistances[neibour[0]][neibour[1]][neibour[2]][neibour[3]])
                                    staggeredList.append(deepCopy(neibour))
                                    #print("    staggerd list:",staggeredList)
    # Add neibours to staggered list
    cellsToUseToUpdate=[item for item in staggeredList]

maximum=0
for I in range(mapCells):
    for J in range(mapCells):
        for i in range(numSeps):
            for j in range(numSeps):
                val=miniCellsDistances[I][J][i][j]
                if val>maximum: maximum=val

print("Max:",maximum)

dx,dy=6,6
def plotWallsIndicator(I,J,i,j):
    center=miniCells[I][J][i][j]
    walls=miniCellsWalls[I][J][i][j]
    if 1 in walls:
        plt.scatter(center[0]-dx,center[1]+dy,c='r')
    if 2 in walls:
        plt.scatter(center[0],center[1]+dy,c='g')
    if 3 in walls:
        plt.scatter(center[0]+dx,center[1]+dy,c='tab:orange')
    if 4 in walls:
        plt.scatter(center[0]-dx,center[1],c='b')
    if 5 in walls:
        plt.scatter(center[0]+dx,center[1],c='c')
    if 6 in walls:
        plt.scatter(center[0]-dx,center[1]-dy,c='y')
    if 7 in walls:
        plt.scatter(center[0],center[1]-dy,c='m')
    if 8 in walls:
        plt.scatter(center[0]+dx,center[1]-dy,c='k')

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
                #plotDistanceIndicator(I,J,i,j)
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
#plt.scatter(absoluteStart[0],absoluteStart[1],c='g')
#plt.scatter(absoluteTarget[0],absoluteTarget[1],c='r')
plt.axis("equal")
plt.show()