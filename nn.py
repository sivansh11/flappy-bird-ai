import random
import math
import pickle
import matrix


class NeuralNetwork:
    def __init__(self, no_of_input_nodes, hidden_layer, no_of_output_nodes):
        self.no_of_input_nodes = no_of_input_nodes
        self.no_of_output_nodes = no_of_output_nodes
        self.hidden_layer = hidden_layer

        self.network = [no_of_input_nodes]
        for i in range(len(hidden_layer)):
            self.network.append(hidden_layer[i])
        self.network.append(no_of_output_nodes)
        self.network_size = len(self.network)

        self.weights = []
        for i in range(self.network_size - 1):
            temp = matrix.Matrix(self.network[i + 1], self.network[i])
            temp.randomize()
            self.weights.append(temp)

        self.biases = []
        for i in range(self.network_size - 1):
            temp = matrix.Matrix(self.network[i + 1], 1)
            temp.randomize()
            self.biases.append(temp)

        self.learning_rate = 0.7

    def predict(self, input_arr):
        if len(input_arr) != self.no_of_input_nodes:
            print('check number of inputs')
            return
        input = matrix.create_matrix(input_arr)

        values = [input]
        for i in range(self.network_size - 2):
            temp = matrix.multiply(self.weights[i], values[i])
            temp.add(self.biases[i])
            temp.map(usefunc_hidden.func)
            values.append(temp)
        i += 1
        output = matrix.multiply(self.weights[i], values[i])
        output.add(self.biases[i])
        output.map(usefunc_output.func)
        return output.ret_arr()

    def show(self):
        print('\n{net}'.format(net = self.network))
        for i in range(len(self.weights)):
            print('weight set', i + 1)
            self.weights[i].show()
        for i in range(len(self.biases)):
            print('bias set', i + 1)
            self.biases[i].show()

    def mutate(self, mutation_rate, mutation_limit):
        lower_limit, upper_limit = mutation_limit
        for x in range(self.network_size - 1):
            for i in range(self.weights[x].rows):
                for j in range(self.weights[x].cols):
                    if random.random() < mutation_rate:
                        self.weights[x].data[i][j] += rand_bet(lower_limit, upper_limit)

        for x in range(self.network_size - 1):
            for i in range(self.biases[x].rows):
                for j in range(self.biases[x].cols):
                    if random.random() < mutation_rate:
                        self.biases[x].data[i][j] += rand_bet(lower_limit, upper_limit)

    def save(self, file):
        pickle.dump(self, file)
        print('saving . . . ')

    def load(self, file):
        temp = pickle.load(file)
        self.no_of_input_nodes = temp.no_of_input_nodes
        self.no_of_output_nodes = temp.no_of_output_nodes
        self.hidden_layer = temp.hidden_layer

        self.network = temp.network
        self.network_size = temp.network_size

        self.weights = temp.weights

        self.biases = temp.biases

        self.learning_rate = temp.learning_rate


    def train(self, input_arr, target_arr):
        inputs = matrix.create_matrix(input_arr)

        # Calculating the values
        values = [inputs]
        for i in range(self.network_size - 2):
            temp = matrix.multiply(self.weights[i], values[i])
            temp.add(self.biases[i])
            temp.map(usefunc_hidden.func)
            values.append(temp)
        i += 1
        outputs = matrix.multiply(self.weights[i], values[i])
        outputs.add(self.biases[i])
        outputs.map(usefunc_output.func)
        ret_output = outputs.ret_arr()
        values.append(outputs)
        # print('showing all values')
        # for v in values:
        #     v.show()
        # print('end -----------------')

        targets = matrix.create_matrix(target_arr)

        error_values = []

        deltas = []

        for i in range(self.network_size - 1):
            j = self.network_size - i
            # error
            if j == self.network_size:
                error = matrix.subtract(targets, outputs)
                error_values.append(error)
            else:
                error = matrix.multiply(matrix.transpose(self.weights[self.network_size - 1 - i]), error_values[i - 1])
                error_values.append(error)
            # gradient
            if j == self.network_size:
                gradient = matrix.map(values[j - 1], usefunc_output.dfunc)
                # print(usefunc_output.dfunc)
            else:
                gradient = matrix.map(values[j - 1], usefunc_hidden.dfunc)
            gradient.multiply(error)
            gradient.multiply(self.learning_rate)
            self.biases[j - 2].add(gradient)
            # calculations of deltas
            weight_deltas = matrix.multiply(gradient, matrix.transpose(values[j - 2]))
            deltas.append(weight_deltas)

        for i in range(len(deltas)):
            self.weights[len(deltas) - 1 - i].add(deltas[i])

        return ret_output


def crossover(nn1, nn2, crossover_rate):
    new = nn1
    for x in range(new.network_size - 1):
        for i in range(new.weights[x].rows):
            for j in range(new.weights[x].cols):
                if random.random() < crossover_rate:
                    new.weights[x].data[i][j] = nn2.weights[x].data[i][j]
    for x in range(new.network_size - 1):
        for i in range(new.biases[x].rows):
            for j in range(new.biases[x].cols):
                if random.random() < crossover_rate:
                    new.biases[x].data[i][j] = nn2.biases[x].data[i][j]
    return new



def sigmoid(v):  # Range of sigmoid is 0 to 1 not -1 to 1
    try:
        return 1 / (1 + math.pow(math.e, -v))
    except OverflowError:
        return 0


def dsigmoid(y):
    return y * (1 - y)


def tanh(v):
    res = math.tanh(v) # output between -1, 1
    return res


def dtanh(y):
    return (1 - y**2)


def map_range(old_range, new_range, s):
    (a1, a2), (b1, b2) = old_range, new_range
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def rand_bet(x, y):
    return map_range((0, 1), (x, y), random.random())


class Func:
    def __init__(self, func=sigmoid, dfunc=sigmoid):
        self.func = func
        self.dfunc = dfunc

    def set_functions(self, func, dfunc):
        self.func = func
        self.dfunc = dfunc


usefunc_hidden = Func(tanh, dtanh)
usefunc_output = Func(sigmoid, dsigmoid)

