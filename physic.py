import vector
import math

speed_limit = math.inf
force_limit = math.inf

class Physics:
    def __init__(self):
        self.position = vector.Vector()
        self.velocity = vector.Vector()
        self.acceleration = vector.Vector()
        self.gravity = vector.Vector(0, 0)
        self.speed_limit = speed_limit
        self.force_limit = force_limit

    def update(self):
        if self.acceleration.mod() > self.force_limit:
            self.acceleration.set_mod(self.force_limit)
        self.velocity.add(self.acceleration)
        if self.velocity.mod() > self.speed_limit:
            self.velocity.set_mod(self.speed_limit)
        self.position.add(self.velocity)
        self.acceleration.multiply(0)

    def applygravity(self):
        self.acceleration.add(self.gravity)