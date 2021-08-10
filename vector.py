import math
import random


class Vector:
    def __init__(self, x=None, y=None, angle=None):
        self.x = x
        self.y = y
        if angle is not None:
            self.create_unit_vector(angle)

        if x is None and angle is None:
            self.create_random_vector()
        if type(x) is Vector:
            self.x = x.x
            self.y = x.y

    def ret_vect(self):
        return self.x, self.y

    def add(self, b):
        a = self
        a.x += b.x
        a.y += b.y

    def ret_add(self, b):
        a = self
        c = Vector(self.x + b.x, self.y + b.y)
        return c

    def sub(self, b):
        a = self
        a.x -= b.x
        a.y -= b.y

    def ret_sub(self, b):
        a = self
        c = Vector(a.x - b.x, a.y - b.y)
        return c

    def ret_coord(self):
        return int(self.x), int(self.y)

    def mod(self):
        return pow(pow(self.x, 2) + pow(self.y, 2), 1/2)

    def ret_angle(self):
        mod = self.mod()
        cos_angle = self.x
        sin_angle = self.y
        #print(sin_angle / mod, cos_angle / mod)
        tan_angle = None
        try:
            tan_angle = sin_angle / cos_angle
            if self.x >= 0 and self.y >= 0:
                return math.atan(tan_angle)
            if self.x < 0 and self.y >= 0:
                return math.atan(tan_angle) + math.pi
            if self.x < 0 and self.y < 0:
                return math.atan(tan_angle) + math.pi
            if self.x >= 0 and self.y < 0:
                return math.atan(tan_angle) + 2 * math.pi
        except ZeroDivisionError:
            if sin_angle > 0:
                return math.pi / 2
            else:
                return (3/2) * math.pi

    def update(self, x, y):
        self.x = x
        self.y = y

    def ret_multiply(self, v):
        b = Vector()
        b.x = v * self.x
        b.y = v * self.y
        return b

    def multiply(self, v):
        self.x *= v
        self.y *= v

    def create_unit_vector(self, angle):
        self.x = math.cos(angle)
        self.y = math.sin(angle)

    def rotate(self, angle):
        new_vec = Vector()
        new_vec.creat_unit_vector(angle)
        new_vec.multiply(self.mod())
        self.x = new_vec.x
        self.y = new_vec.y
        #print(math.degrees(angle))

    def create_random_vector(self):
        #print("random vect")
        angle = random.random()
        angle *= math.pi * 2
        self.create_unit_vector(angle)

    def set_mod(self, v):
        angle = self.ret_angle()
        self.create_unit_vector(angle)
        self.multiply(v)
