from pygame import gfxdraw
import PyGameSetup as pg
import color
import physic

class Pipe:
    def __init__(self, x, y, w, h, screen, gap=300):
        self.phy = physic.Physics()
        self.phy.acceleration.multiply(0)
        self.phy.velocity.update(-2.5, 0)
        self.phy.position.update(x, y)

        self.w = w
        self.h = h
        self.gap = gap
        self.screen = screen

    def show(self):
        x, y = self.phy.position.ret_coord()
        gfxdraw.box(self.screen, ((x, y), (self.w, self.h)), color.green)
        gfxdraw.box(self.screen, ((x, self.h + self.gap), (self.w, pg.height - (self.h + self.gap))), color.green)

    def update(self):
        self.phy.update()

    def collision(self, bird):
        if bird.phy.position.x + bird.r > self.phy.position.x and bird.phy.position.x - bird.r < self.phy.position.x + self.w:
            if bird.phy.position.y - bird.r > self.h and bird.phy.position.y + bird.r < self.h + self.gap:
                return False
            else:
                return True
        else:
            return False

