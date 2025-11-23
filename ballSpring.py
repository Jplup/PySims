import random
import arcade
import numpy as np

WIDTH = 800
HEIGHT = 600
NUM_PARTICLES = 500

mu=0.8

mx=0
my=0

attrK=1

class Ball:
    def __init__(self,x,y,radius=20,mass=1,vx=0,vy=0):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.ax=0
        self.ay=0
        self.m=mass
        self.r=radius
        self.atract=False

    def update(self,fx,fy,dt):

        if self.atract==True:
            dx=(-self.x+mx)
            dy=(-self.y+my)

            d=np.sqrt((dx**2)+(dy**2))

            fax=((d*attrK)*dx)/d
            fay=((d*attrK)*dy)/d
        
            fx+=fax
            fy+=fay

        fx-=self.vx*mu
        fy-=self.vy*mu

        self.ax=fx/self.m
        self.vx+=self.ax*dt
        self.x+=self.vx*dt

        self.ay=fy/self.m
        self.vy+=self.ay*dt
        self.y+=self.vy*dt
        
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1
    
    def draw(self):
        arcade.draw_circle_filled(self.x,self.y,self.r,(255,255,255))

class Spring:
    def __init__(self,restingLenth,ancor1:Ball,ancor2:Ball,k=1):
        self.a1=ancor1
        self.a2=ancor2
        self.l=restingLenth
        self.k=k

    def draw(self):
        arcade.draw_line(self.a1.x,self.a1.y,self.a2.x,self.a2.y,(255,255,255),2)
        self.a1.draw()
        self.a2.draw()

    def update(self,dt):
        
        dx=abs(self.a1.x-self.a2.x)
        dy=abs(self.a1.y-self.a2.y)

        d=np.sqrt((dx**2)+(dy**2))

        fx=(((d-self.l)*self.k)*dx)/d
        fy=(((d-self.l)*self.k)*dy)/d

        if self.a1.x<self.a2.x:
            if self.a1.y<self.a2.y:
                self.a1.update(fx,fy,dt)
                self.a2.update(-fx,-fy,dt)
            else:
                self.a1.update(fx,-fy,dt)
                self.a2.update(-fx,fy,dt)
        else:
            if self.a1.y<self.a2.y:
                self.a1.update(-fx,fy,dt)
                self.a2.update(fx,-fy,dt)
            else:
                self.a1.update(-fx,-fy,dt)
                self.a2.update(fx,fy,dt)

class MySimulation(arcade.Window):
    def __init__(self,spring:Spring):
        super().__init__(WIDTH, HEIGHT, "Particles - Arcade")
        self.spring=spring

    def on_draw(self):
        self.clear()
        self.spring.draw()

    def on_update(self, delta_time):
        self.spring.update(delta_time)

    def on_mouse_motion(self,x,y,dx,dy):
        mx = x
        my = y

    def on_mouse_press(self, x, y, button, modifiers):
        self.spring.a1.atract=True
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.spring.a1.atract=False

if __name__ == "__main__":
    b1=Ball(0.2*WIDTH,0.6*HEIGHT,20,1,0,20)
    b2=Ball(0.85*WIDTH,0.2*HEIGHT)
    s=Spring(0.35*WIDTH,b1,b2,80)
    window = MySimulation(s)
    arcade.run()
