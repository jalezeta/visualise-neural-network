from matplotlib import pyplot
from math import cos, sin, atan


class Neuron():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        circle = pyplot.Circle((self.x, self.y), radius=neuron_radius, fill=False)
        pyplot.gca().add_patch(circle)


class Layer():
    def __init__(self, network, number_of_neurons):
        self.previous_layer = self.__get_previous_layer(network)
        self.y = self.__calculate_layer_y_position()
        self.neurons = self.__intialise_neurons(number_of_neurons)

    def __intialise_neurons(self, number_of_neurons):
        neurons = []
        x = self.__calculate_left_margin_so_layer_is_centered(number_of_neurons)
        for iteration in range(number_of_neurons):
            neuron = Neuron(x, self.y)
            neurons.append(neuron)
            x += horizontal_distance_between_neurons
        return neurons

    def __calculate_left_margin_so_layer_is_centered(self, number_of_neurons):
        return horizontal_distance_between_neurons * (number_of_neurons_in_widest_layer - number_of_neurons) / 2

    def __calculate_layer_y_position(self):
        if self.previous_layer:
            return self.previous_layer.y + vertical_distance_between_layers
        else:
            return 0

    def __get_previous_layer(self, network):
        if len(network.layers) > 0:
            return network.layers[-1]
        else:
            return None

    def __line_between_two_neurons(self, neuron1, neuron2):
        angle = atan((neuron2.x - neuron1.x) / float(neuron2.y - neuron1.y))
        x_adjustment = neuron_radius * sin(angle)
        y_adjustment = neuron_radius * cos(angle)
        line = pyplot.Line2D((neuron1.x - x_adjustment, neuron2.x + x_adjustment), (neuron1.y - y_adjustment, neuron2.y + y_adjustment))
        pyplot.gca().add_line(line)

    def draw(self,sparsity = 0):
        for index, neuron in enumerate(self.neurons):
            neuron.draw()
            if self.previous_layer:
                prev_n_neurons = len(self.previous_layer.neurons)
                sparsity_max_index = max([val for connections in sparsity for val in connections])
                assert (sparsity_max_index <= prev_n_neurons), "One of the sparsity connections is out of index"
                for sparse_neuron_index in sparsity[index]:
                    sparse_neuron = self.previous_layer.neurons[sparse_neuron_index]
                    self.__line_between_two_neurons(neuron, sparse_neuron)


class NeuralNetwork():
    def __init__(self):
        self.layers = []

    def add_layer(self, number_of_neurons):
        layer = Layer(self, number_of_neurons)
        self.layers.append(layer)

    def draw(self,sparsity):
        sparsity_index = 0
        for layer in self.layers:
            if(layer.previous_layer):
                layer.draw(sparsity[sparsity_index])
                sparsity_index = sparsity_index + 1
            else: 
                layer.draw()
        pyplot.axis('scaled')
        pyplot.show()

if __name__ == "__main__":
    vertical_distance_between_layers = 6
    horizontal_distance_between_neurons = 2
    neuron_radius = 0.5
    number_of_neurons_in_widest_layer = 4
    network = NeuralNetwork()
    network.add_layer(3)
    network.add_layer(4)
    network.add_layer(2)
    sparsity_layer0 = [[0,2],[0],[1,2],[0,2]]
    sparsity_layer1 = [[0,2],[2,3]]
    sparsities = [sparsity_layer0,sparsity_layer1]
    network.draw(sparsities)
