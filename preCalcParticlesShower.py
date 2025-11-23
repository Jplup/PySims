import arcade
import numpy as np
import json
import os

WIDTH = 400
HEIGHT = 300

particleSize=2
playbackSpeed=10


class MySimulation(arcade.Window):
    def __init__(self,particles,time):
        super().__init__(WIDTH, HEIGHT, "Particles - Arcade")
        self.particles=particles
        self.timev=time
        self.currentTime=0
        self.ft=time[-1]

    def on_draw(self):
        self.clear()
        i=np.searchsorted(self.timev,self.currentTime)
        for p in self.particles:
            arcade.draw_circle_filled(p[0][i],p[1][i],particleSize/2,(255,255,255))

    def on_update(self, delta_time):
        self.currentTime+=delta_time*playbackSpeed
        if self.currentTime>self.ft: self.currentTime=0

#last="E=20+S=8+N=300+M=0.01+T=10+DT=0.0125+rV=False.json"

show=True

for filename in os.listdir("data"):
    rV=filename.split("+")[-1].split("=")[1].split(".")[0]
    if rV=="True": continue
    print(filename)
    #if filename==last: show=True
    if show:
        with open("data/"+filename) as fs: data=json.load(fs)["data"]
        window = MySimulation(data[0],data[1])
        arcade.run()
