from pygame import gfxdraw
import color
import PyGameSetup as pg
import physic
import random
import nn
import vector
import pygame

output_above = 0.8
net = 5, 5, 3, 1
no_of_inputs = 5
hidden_layer = [3]
no_of_outputs = 1

class Bird:
    def __init__(self, x, y, r, screen):
        self.phy = physic.Physics()
        self.phy.gravity.update(0, 0.5)
        self.phy.force_limit = 3
        self.phy.position.update(x, y)
        self.phy.acceleration.multiply(0)
        self.phy.velocity.multiply(0)

        self.brain = nn.NeuralNetwork(no_of_inputs, hidden_layer, no_of_outputs)

        # self.color = (int(self.brain.weight_HO.data[0][0] * 255), int(self.brain.weight_HO.data[0][1] * 255), int(self.brain.weight_HO.data[0][2] * 255))
        self.color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

        self.r = r

        self.screen = screen

        self.dead = False

        self.score = 0

    def boundrycheck(self):
        if self.phy.position.y > pg.height:
            self.phy.velocity.multiply(0)
            self.phy.acceleration.sub(self.phy.gravity)

        if self.phy.position.y < 0:
            self.phy.velocity.multiply(0)
            self.phy.acceleration.multiply(0)
            self.phy.acceleration.add(self.phy.gravity)

    def update(self):
        self.phy.applygravity()
        self.boundrycheck()
        self.phy.update()
        self.score += 1

    def applyforce(self):
        force = vector.Vector(0, -4)
        self.phy.acceleration.add(force)

    def show(self):
        x, y = self.phy.position.ret_coord()
        gfxdraw.filled_circle(self.screen, x, y, self.r, self.color)

    def think(self, inputs):
        outputs = self.brain.predict(inputs)
        if outputs[0] > output_above:
            self.applyforce()


def newcol(p1, p2):
    x1,y1,z1 = p1
    x2,y2,z2 = p2
    return (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
