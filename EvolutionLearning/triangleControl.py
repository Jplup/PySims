import arcade
import numpy as np

WIDTH = 800
HEIGHT = 600
dy=10
dx=7
numOfAgents=1
moveSpeed=300
rotationSpeed=5

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

def CalculatePointsPositionAndDraw(center,angle):
    newPositions=[]
    for i in range(3):
        newPositions.append([
                np.cos(angles[i]+angle)*distances[i]+center[0],
                np.sin(angles[i]+angle)*distances[i]+center[1]
        ])

    arcade.draw_line(newPositions[0][0],newPositions[0][1],newPositions[1][0],newPositions[1][1],[255,255,255])
    arcade.draw_line(newPositions[1][0],newPositions[1][1],newPositions[2][0],newPositions[2][1],[255,255,255])
    arcade.draw_line(newPositions[2][0],newPositions[2][1],newPositions[0][0],newPositions[0][1],[255,255,255])


agents=[[WIDTH/2,HEIGHT/2,0,0,np.deg2rad(90)] for _ in range(numOfAgents)]

class MySimulation(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Evo - Arcade")
        self.moveCommand=[0,0]
        
    def on_draw(self):
        self.clear()
        for agent in agents:
            CalculatePointsPositionAndDraw([agent[0],agent[1]],agent[4])
            

    def on_update(self, delta_time):
        for agent in agents:
            agent[2]=self.moveCommand[0]
            agent[3]=self.moveCommand[1]

        for agent in agents:
            agent[4]+=agent[2]*delta_time*rotationSpeed
            agent[0]+=np.cos(agent[4])*agent[3]*moveSpeed*delta_time
            agent[1]+=np.sin(agent[4])*agent[3]*moveSpeed*delta_time
    
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

    '''def on_mouse_motion(self,x,y,dx,dy):
        mx = x
        my = y

    def on_mouse_press(self, x, y, button, modifiers):
        self.spring.a1.atract=True
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.spring.a1.atract=False'''

if __name__ == "__main__":
    window = MySimulation()
    arcade.run()