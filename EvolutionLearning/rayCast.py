import arcade
import numpy as np

WIDTH = 800
HEIGHT = 500
dy=40
dx=28
numOfAgents=1
moveSpeed=80
rotationSpeed=5
debugBallSize=3
numberOfRays=2
raioDeSeparacaoAteRaios=5
maxRayAngle=np.deg2rad(60)
rayDistance=80

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

agents=[[WIDTH/2,HEIGHT/2,0,0,np.deg2rad(90),[[0,0],[0,0],[0,0]]] for _ in range(numOfAgents)]

rays=[[[[0,0],[0,0],[0,0]] for _ in range(numberOfRays*2+1)] for _ in range(numOfAgents)]

lineObstacles=[
    [[WIDTH/3,HEIGHT/4],[WIDTH/3,3*HEIGHT/4]],
    [[1*WIDTH/5,HEIGHT/2],[4*WIDTH/5,HEIGHT/2]],
    [[1*WIDTH/5,HEIGHT/2-50],[4*WIDTH/5,HEIGHT/2]]
]

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

def DoRayCasts():
    for i in range(numOfAgents):
        for j in range(2*numberOfRays+1):
            for lineObstacle in lineObstacles:
                ray=rays[i][j]
                x,y,result=RayCast(ray,lineObstacle)
                if result==True: arcade.draw_circle_filled(x,y,debugBallSize,[255,0,0])


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
        
    
    def on_update(self, delta_time):
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