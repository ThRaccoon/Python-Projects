import math
import ast
import random
from cpu_training.fromScratch_version.rMath import Rmath


# Classes ==============================================================================================================
class InitParams:
    @staticmethod
    def create_inputs(n_batches: int, n_inputs: int):
        output_matrix = []

        for _i in range(n_batches):
            output_matrix.append([])
            for _j in range(n_inputs):
                output_matrix[_i].append(random.choice([0, 1]))
        return output_matrix

    @staticmethod
    def create_weights(n_inputs: int, n_neurons: int):
        output_matrix = []

        # Standard deviation (specifically "He" initialization)
        # Prevent vanishing or exploding gradients by setting the weights in the range (0, std_dev)
        std_dev = math.sqrt(2 / n_inputs)

        for _i in range(n_inputs):
            output_matrix.append([])
            for _j in range(n_neurons):
                output_matrix[_i].append(random.gauss(0, std_dev))
        return output_matrix

    @staticmethod
    def create_biases(weight_matrix: list[list[int | float]] | list[int | float]):
        output_vector = []

        for _i in range(len(weight_matrix[0])):
            output_vector.append(0)
        return output_vector


class LayerDense:
    instance_counter = 1

    def __init__(self, n_inputs: int, n_neurons: int, load_from_file=False):
        # Forward
        self.weights = []
        self.biases = []
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons
        self.output_matrix = []

        # Backward
        self.g_weights = []
        self.g_biases = []

        # Instance counter
        self.id = LayerDense.instance_counter
        LayerDense.instance_counter += 1

        if load_from_file:
            try:
                self.read_from_file()
                print(f"Weights and biases for L{self.id} were loaded from a file!")
            except FileNotFoundError:
                self.weights.clear()
                self.biases.clear()
                print(f"Weights and biases for L{self.id} were randomly created!")
                self.create_random_weights_and_biases()
        else:
            self.create_random_weights_and_biases()
            print(f"Weights and biases for L{self.id} were randomly created!")

    def forward(self, input_matrix: list[list[int | float]] | list[int | float]):

        # Computes the output of this layer by performing a matrix multiplication
        # of the input matrix with the layer's weights and adding the biases
        self.output_matrix = rmath.matrix_product_with_bias(input_matrix, self.weights, self.biases)

    def backward(self, relu_output: list[list[int | float] | list[int | float]],
                 g_activation_output: list[list[int | float]] | list[int | float]):

        # Calculating gradients for weights and biases
        self.g_weights = rmath.matrix_product(rmath.matrix_transpose(relu_output), g_activation_output)
        self.g_biases = rmath.matrix_column_sum(g_activation_output)

        # Performing gradient clipping
        # Maximum allowed norm for gradients (best between 1 - 5)
        max_norm = 2

        # Weights
        sqrt_sum = 0
        for _i in range(len(self.g_weights)):
            for _j in range(len(self.g_weights[0])):
                sqrt_sum += self.g_weights[_i][_j] ** 2

        current_norm_weights = math.sqrt(sqrt_sum)  # L2 norm

        if max_norm < current_norm_weights:
            scaling_factor_weights = max_norm / current_norm_weights  # Factor to scale gradients
            for _i in range(len(self.g_weights)):
                for _j in range(len(self.g_weights[0])):
                    self.g_weights[_i][_j] *= scaling_factor_weights

        # Biases
        sqrt_sum = 0
        for _i in range(len(self.g_biases)):
            sqrt_sum += self.g_biases[_i] ** 2

        current_norm_biases = math.sqrt(sqrt_sum)  # L2 norm

        if max_norm < current_norm_biases:
            scaling_factor_biases = max_norm / current_norm_biases  # Factor to scale gradients
            for _i in range(len(self.g_biases)):
                self.g_biases[_i] *= scaling_factor_biases

    def update(self, learning_rate: int | float, lambda_val: int | float):

        # Applying L2 regularization (only to weights)
        # Update rule with L2 regularization: weight = weight - lr * (weight_grad + lambda * weight)

        # Updating weights
        for _i in range(len(self.weights)):
            for _j in range(len(self.weights[0])):
                self.weights[_i][_j] -= learning_rate * (self.g_weights[_i][_j] + lambda_val * self.weights[_i][_j])

        # Update biases
        for _i in range(len(self.biases)):
            self.biases[_i] -= learning_rate * self.g_biases[_i]

    def write_to_file(self, mode: str):
        with open("files/weights.txt", mode) as w_file:
            w_file.write(f"{self.id}\n")
            w_file.write(f"{self.weights}\n")

        print(f"L{self.id} weights were updated!")

        with open("files/biases.txt", mode) as b_file:
            b_file.write(f"{self.id}\n")
            b_file.write(f"{self.biases}\n")

        print(f"L{self.id} biases were updated!")

    def read_from_file(self):
        self.read_weights_from_file()
        self.read_biases_from_file()

    def read_weights_from_file(self):
        checker = False
        try:
            with open("files/weights.txt", "r") as w_file:
                for _line in w_file:
                    if _line.startswith(str(self.id)):
                        self.weights = ast.literal_eval(next(w_file))
                        checker = True
                        break
                if not checker:
                    raise FileNotFoundError
        except FileNotFoundError:
            print(f"File don't exist or L{self.id} weights are missing from the file!")
            raise FileNotFoundError

    def read_biases_from_file(self):
        checker = False
        try:
            with open("files/biases.txt", "r") as b_file:
                for _line in b_file:
                    if _line.startswith(str(self.id)):
                        self.biases = ast.literal_eval(next(b_file))
                        checker = True
                        break
                if not checker:
                    raise FileNotFoundError
        except FileNotFoundError:
            print(f"File don't exist or L{self.id} biases are missing from the file!")
            raise FileNotFoundError

    def create_random_weights_and_biases(self):
        self.weights = init.create_weights(self.n_inputs, self.n_neurons)
        self.biases = init.create_biases(self.weights)


class ActivationReLU:
    def __init__(self):
        # Forward
        self.input_matrix = []
        self.output_matrix = []

        # Backward
        self.g_relu_input = []
        self.g_relu_output = []

    def forward(self, input_matrix: list[list[int | float]] | list[int | float]):

        # Saving the input matrix for later use (in backpropagation)
        self.input_matrix = input_matrix

        # Applying the ReLU function to each element of the input_matrix
        self.output_matrix = []
        for _i in range(len(input_matrix)):
            self.output_matrix.append([])
            for _j in range(len(input_matrix[0])):
                if input_matrix[_i][_j] <= 0:
                    self.output_matrix[_i].append(0)
                else:
                    self.output_matrix[_i].append(input_matrix[_i][_j])

    def backward(self, g_activation_output: list[list[int | float]] | list[int | float],
                 weights: list[list[int | float]] | list[int | float]):

        # Calculating gradients for relu input (since it's backward it's from right to left)
        self.g_relu_input = rmath.matrix_product(g_activation_output, rmath.matrix_transpose(weights))

        # Calculating gradients for relu output
        d_relu = []
        for _i in range(len(self.input_matrix)):
            d_relu.append([])
            for _j in range(len(self.input_matrix[0])):
                if self.input_matrix[_i][_j] <= 0:
                    d_relu[_i].append(0)
                else:
                    d_relu[_i].append(1)

        # Performing element wise multiplication
        self.g_relu_output = rmath.matrix_mul(d_relu, self.g_relu_input)


class ActivationSoftmax:
    def __init__(self):
        # Forward
        self.output_matrix = []

        # Backward
        self.g_softmax_output = []

    def forward(self, input_matrix: list[list[int | float]] | list[int | float]):

        # Applying the Softmax function to each element of the input_matrix

        # Euler number
        e = 2.7182818
        epsilon = 1e-9  # Small value to prevent division by zero
        self.output_matrix = []

        # Subtracting the max value of each row to prevent overflow
        for _i in range(len(input_matrix)):
            self.output_matrix.append([])
            max_value = max(input_matrix[_i])
            for _j in range(len(input_matrix[0])):
                self.output_matrix[_i].append(input_matrix[_i][_j] - max_value)

        # Performing element-wise exponentiation
        for _i in range(len(self.output_matrix)):
            for _j in range(len(self.output_matrix[0])):
                self.output_matrix[_i][_j] = e ** self.output_matrix[_i][_j]

        # Performing normalization
        for _i in range(len(self.output_matrix)):
            # Adding epsilon to exp_value to avoid division by zero
            exp_value = sum(self.output_matrix[_i]) + epsilon
            for _j in range(len(self.output_matrix[0])):
                self.output_matrix[_i][_j] /= exp_value

    def backward(self, y_true: list[int | float]):

        # Calculating gradients for softmax output
        self.g_softmax_output = []
        for _i in range(len(self.output_matrix)):
            self.g_softmax_output.append([])
            for _j in range(len(self.output_matrix[0])):
                if _j == y_true[_i]:
                    self.g_softmax_output[_i].append(self.output_matrix[_i][_j] - 1)
                else:
                    self.g_softmax_output[_i].append(self.output_matrix[_i][_j])


class CrossEntropyLoss:
    def __init__(self):
        self.avg_loss = 0

    def forward(self, y_pre: list[list[int | float]], y_true: list[int | float]):

        epsilon = 1e-9  # Small value to prevent division by zero

        # Compute the cross-entropy loss
        cross_entropy_losses = []
        for _i in range(len(y_pre)):
            # Ensure the predicted probability is not zero to avoid log(0)
            prob = y_pre[_i][y_true[_i]]
            if prob == 0:
                prob = epsilon
            cross_entropy_losses.append(-math.log(prob))

        # Compute the average cross-entropy loss
        self.avg_loss = sum(cross_entropy_losses) / len(cross_entropy_losses)


class Accuracy:
    def __init__(self):
        self.accuracy = 0

    def forward(self, y_pre: list[list[int | float]], y_true: list[int | float]):

        correct_count = 0
        predicted_labels = []

        # Collect the predicted label index by appending the index of the highest prediction score
        for _i in range(len(y_pre)):
            _counter = 0
            _temp = 0
            for _j in range(1, len(y_pre[0])):
                if y_pre[_i][_counter] < y_pre[_i][_j]:
                    _temp = _j
                _counter += 1
            predicted_labels.append(_temp)

        # Compare the predicted labels with the true labels
        for _i in range(len(y_true)):
            if y_true[_i] == predicted_labels[_i]:
                correct_count += 1

        # Calculate accuracy
        self.accuracy = correct_count / len(y_true)


# Functions ============================================================================================================
def forward_loop():
    layer1.forward(X)
    relu1.forward(layer1.output_matrix)

    layer2.forward(relu1.output_matrix)
    relu2.forward(layer2.output_matrix)

    layer3.forward(relu2.output_matrix)
    relu3.forward(layer3.output_matrix)

    layer4.forward(relu3.output_matrix)
    relu4.forward(layer4.output_matrix)

    layer5.forward(relu4.output_matrix)
    relu5.forward(layer5.output_matrix)

    layer6.forward(relu5.output_matrix)
    relu6.forward(layer6.output_matrix)

    layer7.forward(relu6.output_matrix)
    softmax1.forward(layer7.output_matrix)

    loss.forward(softmax1.output_matrix, y)
    accuracy.forward(softmax1.output_matrix, y)

    print("Loss:", loss.avg_loss)
    print("Accuracy:", accuracy.accuracy)


def backward_update_loop():
    softmax1.backward(y)
    layer7.backward(relu6.output_matrix, softmax1.g_softmax_output)
    layer7.update(lr, lambda_str)

    relu6.backward(softmax1.g_softmax_output, layer7.weights)
    layer6.backward(relu5.output_matrix, relu6.g_relu_output)
    layer6.update(lr, lambda_str)

    relu5.backward(relu6.g_relu_output, layer6.weights)
    layer5.backward(relu4.output_matrix, relu5.g_relu_output)
    layer5.update(lr, lambda_str)

    relu4.backward(relu5.g_relu_output, layer5.weights)
    layer4.backward(relu3.output_matrix, relu4.g_relu_output)
    layer4.update(lr, lambda_str)

    relu3.backward(relu4.g_relu_output, layer4.weights)
    layer3.backward(relu2.output_matrix, relu3.g_relu_output)
    layer3.update(lr, lambda_str)

    relu2.backward(relu3.g_relu_output, layer3.weights)
    layer2.backward(relu1.output_matrix, relu2.g_relu_output)
    layer2.update(lr, lambda_str)

    relu1.backward(relu2.g_relu_output, layer2.weights)
    layer1.backward(X, relu1.g_relu_output)
    layer1.update(lr, lambda_str)


def update_file():
    layer1.write_to_file("w")
    layer2.write_to_file("a")
    layer3.write_to_file("a")
    layer4.write_to_file("a")
    layer5.write_to_file("a")
    layer6.write_to_file("a")
    layer7.write_to_file("a")


# Init =================================================================================================================
init = InitParams()
rmath = Rmath()

# Create random inputs
# X = init.create_inputs(20, 400)

# Sparse
# y = [0, 1, 2]
# y = check_dimensions(y)

# One-hot
# y1 = [[1, 0, 0]
#       [0, 1, 0]
#       [0, 0, 1]

# Learning rate
lr = 0.0005

# Lambda strength (L2 regularization strength)
lambda_str = 0.001


# Neural network architecture ==========================================================================================
layer1 = LayerDense(784, 512, False)
relu1 = ActivationReLU()

layer2 = LayerDense(512, 256, False)
relu2 = ActivationReLU()

layer3 = LayerDense(256, 128, False)
relu3 = ActivationReLU()

layer4 = LayerDense(128, 64, False)
relu4 = ActivationReLU()

layer5 = LayerDense(64, 32, False)
relu5 = ActivationReLU()

layer6 = LayerDense(32, 16, False)
relu6 = ActivationReLU()

layer7 = LayerDense(16, 10, False)
softmax1 = ActivationSoftmax()

loss = CrossEntropyLoss()
accuracy = Accuracy()


# Loading training data from file ======================================================================================
file_lines = []
with open("../../training&testing_data/formatted_training_data.csv", "r") as file:
    for line in file:
        file_lines.append(ast.literal_eval(line.strip()))

# The number of images per epoch
batch_ranges = ((0, 199), (200, 399), (400, 599), (600, 799), (800, 999), (1000, 1199), (1200, 1399), (1400, 1599),
                (1600, 1799), (1800, 1999), (2000, 2199), (2200, 2399), (2400, 2599), (2600, 2799), (2800, 2999))


pixel_batches = []
for i in range(len(batch_ranges)):
    st, ed = batch_ranges[i]
    pixel_batches.append([])
    for j in range(st, ed):
        pixel_batches[i].append(file_lines[j])

file_lines.clear()

# Inputs (AKA pixels)
X = []

# True labels (AKA answers)
y = []

breaker = 0
counter = 0

# Forward - Backward & Update ==========================================================================================
while True:

    if counter == len(batch_ranges):
        counter = 0
        print("------------------------------")

    random.shuffle(pixel_batches[counter])

    for i in range(len(pixel_batches[0])):
        temp = pixel_batches[counter][i]
        X.append(temp[:-1])
        y.append(temp[-1] - 1)

    print(counter)
    forward_loop()
    backward_update_loop()

    if breaker == 3000:
        print("Write 'Exit' to save the weights and biases to file and exit the program")
        print("or write anything else to continue learning without saving")
        user_inp = input(":")
        if user_inp == "Exit":
            update_file()
            exit(0)
        else:
            breaker = 0

    counter += 1
    breaker += 1

    X.clear()
    y.clear()
