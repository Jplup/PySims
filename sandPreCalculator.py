import random
import json

WIDTH=600
HEIGHT=600

scaleFactor=10

changesPerSecond=1200
freq=1/changesPerSecond

maxFPS=60

drawsPerSecond=changesPerSecond if changesPerSecond<maxFPS else maxFPS
drawRate=1/drawsPerSecond
print("Freq:",freq,"draw")

randomGrains=True

colors=[(0,0,0),(0,255,0),(180,180,0),(255,0,0)]

class MySimulation():
    def __init__(self):
        self.w=int(WIDTH/scaleFactor)
        self.h=int(HEIGHT/scaleFactor)
        self.cells=[[0 for _ in range(self.h)] for _ in range(self.w)]
        self.cellss=[[[0] for _ in range(self.h)] for _ in range(self.w)]

    def Tumble(self,i,j,numberOfIterations=0):
        if numberOfIterations>500: return
        if self.cells[i][j]>3:
            self.cells[i][j]-=4
            if i-1>0:
                self.cells[i-1][j]+=1
                if self.cells[i-1][j]>3: self.Tumble(i-1,j,numberOfIterations+1)
            if i+1<self.w:
                self.cells[i+1][j]+=1
                if self.cells[i+1][j]>3: self.Tumble(i+1,j,numberOfIterations+1)
            if j-1>0:
                self.cells[i][j-1]+=1
                if self.cells[i][j-1]>3: self.Tumble(i,j-1,numberOfIterations+1)
            if j+1<self.h:
                self.cells[i][j+1]+=1
                if self.cells[i][j+1]>3: self.Tumble(i,j+1,numberOfIterations+1)

    def update(self):
        if randomGrains: newGrain=[random.randint(1,self.w-1),random.randint(1,self.h-1)]
        else: newGrain=[int(self.w/2),int(self.h/2)]
        self.cells[newGrain[0]][newGrain[1]]+=1
        for i in range(self.w):
            for j in range(self.h):
                self.Tumble(i,j)
    
    def run(self,numSteps,directory):
        for k in range(numSteps):
            print(100*(k/numSteps),"%")
            self.update()
            for i in range(self.w):
                for j in range(self.h):
                    self.cellss[i][j].append(self.cells[i][j])
        with open(directory,'w') as fs: json.dump({"a":self.cellss},fs)

                    

if __name__ == "__main__":
    obj=MySimulation()
    obj.run(10000,'sand.json')

