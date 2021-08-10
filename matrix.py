import random


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = list()

        for i in range(self.rows):
            temp = list()
            for j in range(self.cols):
                temp.append(0)
            self.data.append(temp)

    def show(self):
        print("-----------------------")
        print(str(self.rows) + "x" + str(self.cols))
        for i in range(self.rows):
            print(self.data[i])
        print("-----------------------")

    def randomize(self, lower_limit=-1, upper_limit=1):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = rand_bet(lower_limit, upper_limit)

    def add(self, v):
        if type(v) is Matrix:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += v.data[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += v

    def subtract(self, v):
        if type(v) is Matrix:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] -= v.data[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] -= v

    def multiply(self, v):
        if type(v) is Matrix:
            # Matrix multiplication
            for i in range(self.rows):
                for j in range(v.cols):
                    self.data[i][j] *= v.data[i][j]
        else:
            # scalar multiplication
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] *= v

    def map(self, func):
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.data[i][j]
                self.data[i][j] = func(val)

    def ret_arr(self):
        arr = []
        for i in range(self.rows):
            for j in range(self.cols):
                arr.append(self.data[i][j])
        return arr


def transpose(a):
    result = Matrix(a.cols, a.rows)
    for i in range(a.rows):
        for j in range(a.cols):
            result.data[j][i] = a.data[i][j]
    return result


def create_matrix(arr):
    m = Matrix(len(arr), 1)
    for i in range(len(arr)):
        m.data[i][0] = arr[i]
    return m


def multiply(a, b):
    if type(b) is Matrix:
        # Matrix multiplication
        if a.cols != b.rows:
            print("col of A does not match rows of B")
            return None
        result = Matrix(a.rows, b.cols)
        for i in range(result.rows):
            for j in range(result.cols):
                element = 0
                for k in range(a.cols):
                    element += a.data[i][k] * b.data[k][j]
                result.data[i][j] = element
        return result
    else:
        # scalar multiplication
        result = Matrix(a.rows, a.cols)
        for i in range(a.rows):
            for j in range(a.cols):
                result.data[i][j] = a.data[i][j] * b
        return a


def add(a, b):
    if type(b) is Matrix:
        result = Matrix(a.rows, a.cols)
        for i in range(a.rows):
            for j in range(a.cols):
                result.data[i][j] = a.data[i][j] + b.data[i][j]
        return result
    else:
        result = Matrix(a.rows, a.cols)
        for i in range(a.rows):
            for j in range(a.cols):
                result = a.data[i][j] + b
        return result


def subtract(a, b):
    if type(b) is Matrix:
        result = Matrix(a.rows, a.cols)
        for i in range(a.rows):
            for j in range(a.cols):
                result.data[i][j] = a.data[i][j] - b.data[i][j]
        return result
    else:
        result = Matrix(a.rows, a.cols)
        for i in range(a.rows):
            for j in range(a.cols):
                result = a.data[i][j] - b
        return result


def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def rand_bet(x, y):
    return maprange((0, 1), (x, y), random.random())


def map(arr, func):
    for i in range(arr.rows):
        for j in range(arr.cols):
            val = arr.data[i][j]
            arr.data[i][j] = func(val)
    return arr
