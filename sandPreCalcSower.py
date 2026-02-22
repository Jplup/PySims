import arcade
import json

WIDTH=600
HEIGHT=600

scaleFactor=10

changesPerSecond=60
freq=1/changesPerSecond

maxFPS=60

drawsPerSecond=changesPerSecond if changesPerSecond<maxFPS else maxFPS
drawRate=1/drawsPerSecond

randomGrains=True
iterationsPerTimeTick=20

colors=[(0,0,0),(0,255,0),(180,180,0),(255,0,0)]

with open('sand.json') as fs:
    dic=json.load(fs)
    data=dic["a"]

class MySimulation(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Particles - Arcade",update_rate=freq,draw_rate=drawRate)
        self.w=int(WIDTH/scaleFactor)
        self.h=int(HEIGHT/scaleFactor)
        self.iterIdx=0
        self.maxIters=len(data[0][0])

    def on_draw(self):
        self.clear()
        for i in range(self.w):
            for j in range(self.h):
                center=data[i][j][self.iterIdx]
                if center<1:
                    if center==0: pass
                    else: arcade.draw_point(i*scaleFactor,j*scaleFactor,(255,255,255),scaleFactor)
                else:
                    if center>=4:
                        arcade.draw_point(i*scaleFactor,j*scaleFactor,(0,0,255),scaleFactor)
                    else:
                        arcade.draw_point(i*scaleFactor,j*scaleFactor,colors[int(center)],scaleFactor)

    def on_update(self, delta_time):
        self.iterIdx+=iterationsPerTimeTick
        if self.iterIdx>self.maxIters: self.iterIdx=0
                    

if __name__ == "__main__":
    window = MySimulation()
    arcade.run()
