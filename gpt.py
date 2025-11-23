import random
import arcade

WIDTH = 800
HEIGHT = 600
NUM_PARTICLES = 500

class Particle:
    def __init__(self):
        self.x = random.random() * WIDTH
        self.y = random.random() * HEIGHT
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-10, 10)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1

class MySimulation(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Particles - Arcade")
        self.particles = [Particle() for _ in range(NUM_PARTICLES)]

    def on_draw(self):
        self.clear()
        for p in self.particles:
            arcade.draw_point(p.x, p.y, arcade.color.YELLOW, 1)

    def on_update(self, delta_time):
        for p in self.particles:
            p.update()

if __name__ == "__main__":
    window = MySimulation()
    arcade.run()
