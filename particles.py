import random
import arcade
import numpy as np

WIDTH = 800
HEIGHT = 600

particleSize=20
epsilon=0.2*100 # Force maximum
sigma=5 # Static distance
numParticles=100

maxVel=100

randomVels=True
iniVel=1

class Particle:
    def __init__(self,x,y,mass=0.8*10,vx=0,vy=0):
        self.x=x
        self.y=y
        if randomVels:
            self.vx=random.randint(-iniVel,iniVel)
            self.vy=random.randint(-iniVel,iniVel)
        else:
            self.vx=0
            self.vy=0
        self.ax=0
        self.ay=0
        self.m=mass
        self.r=particleSize/2
        self.fx=0
        self.fy=0

    @staticmethod
    def SaturateValues(value,maximums=[-maxVel,maxVel]):
        if value<maximums[0]: return maximums[0]
        if value>maximums[1]: return maximums[1]
        return value

    def update(self,dt):
        #fx-=self.vx*mu
        #fy-=self.vy*mu

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

        self.fx=0
        self.fy=0
    
    def draw(self):
        arcade.draw_circle_filled(self.x,self.y,self.r,(255,255,255))

def CalculateForces(p1,p2):
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    d=np.sqrt((dx**2)+(dy**2))
    if dx==0: dx=0.0001
    if dy==0: dy=0.0001
    F=(24*epsilon/(d**2))*(((sigma/d)**6)-(2*((sigma/d)**12)))

    return F*dx/d,F*dy/d

class MySimulation(arcade.Window):
    def __init__(self,n):
        super().__init__(WIDTH, HEIGHT, "Particles - Arcade")
        self.particles=[]
        for _ in range(n):
            for _ in range(100):
                x=(random.random()*(WIDTH-30))+15
                y=(random.random()*(HEIGHT-30))+15
                #self.vx = random.uniform(-10, 10)
                #self.vy = random.uniform(-10, 10)
                tooClose=False
                for other in self.particles:
                    dx=x-other.x
                    dy=y-other.y
                    d=np.sqrt((dx**2)+(dy**2))
                    if d<particleSize*4:
                        tooClose=True
                        break
                if not tooClose:
                    self.particles.append(Particle(x,y))
                    break 

    def on_draw(self):
        self.clear()
        for p in self.particles: p.draw()

    @staticmethod
    def UnZero(value):
        if value==0: return 0.0001
        else: return value
    
    @staticmethod
    def ForceFromDistance(d):
        return -(24*epsilon/(d**2))*(((sigma/d)**6)-(2*((sigma/d)**12)))

    def on_update(self, delta_time):
        size=len(self.particles)
        for i in range(size):
            for j in range(size-1-i):
                p1=self.particles[i]
                p2=self.particles[j+1+i]
                fx,fy=CalculateForces([p1.x,p1.y],[p2.x,p2.y])
                p1.fx+=fx
                p1.fy+=fy
                p2.fx-=fx
                p2.fy-=fy
        for p in self.particles:
            dxl=self.UnZero(p.x)
            dxr=self.UnZero(WIDTH-p.x)
            dyd=self.UnZero(p.y)
            dyu=self.UnZero(HEIGHT-p.y)
            Fx=self.ForceFromDistance(dxl)-self.ForceFromDistance(dxr)
            Fy=self.ForceFromDistance(dyd)-self.ForceFromDistance(dyu)
            p.fx+=Fx
            p.fy+=Fy
        for p in self.particles: p.update(delta_time)

'''    def on_mouse_motion(self,x,y,dx,dy):
        mx = x
        my = y

    def on_mouse_press(self, x, y, button, modifiers):
        self.spring.a1.atract=True
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.spring.a1.atract=False'''

if __name__ == "__main__":
    window = MySimulation(numParticles)
    arcade.run()
