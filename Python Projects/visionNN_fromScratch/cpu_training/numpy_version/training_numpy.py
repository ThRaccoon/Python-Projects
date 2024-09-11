import math
import ast
import random
import numpy as np


# Classes ==============================================================================================================
class InitParams:
    @staticmethod
    def create_inputs(n_batches: int, n_inputs: int):

        output_matrix = np.random.random((n_batches, n_inputs))

        return output_matrix

    @staticmethod
    def create_weights(n_inputs: int, n_neurons: int):

        # Standard deviation (specifically "He" initialization)
        # Prevent vanishing or exploding gradients by setting the weights in the range (0, std_dev)
        std_dev = math.sqrt(2 / n_inputs)

        output_matrix = np.random.normal(0, std_dev, (n_inputs, n_neurons))

        return output_matrix

    @staticmethod
    def create_biases(weight_matrix: np.ndarray):

        output_vector = np.zeros(weight_matrix.shape[1])

        return output_vector


class LayerDense:
    instance_counter = 1

    def __init__(self, n_inputs: int, n_neurons: int, load_from_file=False):
        # Forward
        self.weights = np.empty((0, 0))
        self.biases = np.empty(0)
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons
        self.output_matrix = np.empty((0, 0))

        # Backward
        self.g_weights = np.empty((0, 0))
        self.g_biases = np.empty((0, 0))

        # Instance counter
        self.id = LayerDense.instance_counter
        LayerDense.instance_counter += 1

        if load_from_file:
            try:
                self.read_weights_and_biases_from_file()
                print(f"Weights and biases for L{self.id} were loaded from a file!")
            except (FileNotFoundError, EOFError):
                print(f"L{self.id} Weights and biases are missing from the file or the file is missing!")
                self.create_random_weights_and_biases()
                print(f"Weights and biases for L{self.id} were randomly created!")
        else:
            self.create_random_weights_and_biases()
            print(f"Weights and biases for L{self.id} were randomly created!")

    def forward(self, input_matrix: np.ndarray):

        # Computes the output of this layer by performing a matrix multiplication
        # of the input matrix with the layer's weights and adding the biases
        self.output_matrix = np.dot(input_matrix, self.weights) + self.biases

    def backward(self, relu_output: np.ndarray, g_activation_output: np.ndarray):

        # Calculating gradients for weights and biases
        self.g_weights = np.dot(relu_output.T, g_activation_output)
        self.g_biases = np.sum(g_activation_output, axis=0)

        # Performing gradient clipping

        # Maximum allowed norm for gradients (best between 1 - 5)
        max_norm = 2

        # Weights
        sqrt_sum = np.sum(self.g_weights ** 2)

        current_norm_weights = math.sqrt(sqrt_sum)  # L2 norm

        if max_norm < current_norm_weights:
            scaling_factor_weights = max_norm / current_norm_weights  # Factor to scale gradients
            self.g_weights *= scaling_factor_weights

        # Biases
        sqrt_sum = np.sum(self.g_biases ** 2)

        current_norm_biases = math.sqrt(sqrt_sum)  # L2 norm

        if max_norm < current_norm_biases:
            scaling_factor_biases = max_norm / current_norm_biases  # Factor to scale gradients
            self.g_biases *= scaling_factor_biases

    def update(self, learning_rate: int | float, lambda_val: int | float):

        # Applying L2 regularization (only to weights)
        # Update rule with L2 regularization: weight = weight - lr * (weight_grad + lambda * weight)

        # Updating weights
        self.weights -= learning_rate * (self.g_weights + lambda_val * self.weights)

        # Update biases
        self.biases -= learning_rate * self.g_biases

    def read_weights_and_biases_from_file(self):
        with np.load("files/weights&biases_np.npz") as _file:
            self.weights = _file[f"l{self.id}_w"]
            self.biases = _file[f"l{self.id}_b"]

    def create_random_weights_and_biases(self):
        self.weights = init.create_weights(self.n_inputs, self.n_neurons)
        self.biases = init.create_biases(self.weights)


class ActivationReLU:
    def __init__(self):
        # Forward
        self.input_matrix = np.empty((0, 0))
        self.output_matrix = np.empty((0, 0))

        # Backward
        self.g_relu_input = np.empty((0, 0))
        self.g_relu_output = np.empty((0, 0))

    def forward(self, input_matrix: np.ndarray):

        # Saving the input matrix for later use (in backpropagation)
        self.input_matrix = input_matrix

        # Applying the ReLU function to each element of the input_matrix
        self.output_matrix = np.maximum(0, input_matrix)

    def backward(self, g_activation_output: np.ndarray,
                 weights: np.ndarray):

        # Calculating gradients for relu input (since it's backward it's from right to left)
        self.g_relu_input = np.dot(g_activation_output, weights.T)

        # Calculating gradients for relu output
        d_relu = np.where(self.input_matrix > 0, 1, 0)

        # Performing element wise multiplication
        self.g_relu_output = d_relu * self.g_relu_input


class ActivationSoftmax:
    def __init__(self):
        # Forward
        self.output_matrix = np.empty((0, 0))

        # Backward
        self.g_softmax_output = np.empty((0, 0))

    def forward(self, input_matrix: np.ndarray):

        # Applying the Softmax function to each element of the input_matrix

        # Euler number
        e = 2.7182818
        epsilon = 1e-9  # Small value to prevent division by zero
        self.output_matrix = np.empty((0, 0))

        # Subtracting the max value of each row to prevent overflow
        max_value = np.max(input_matrix, axis=1)

        # Reshape it to make it column vector
        max_value = np.reshape(max_value, (-1, 1))

        self.output_matrix = input_matrix - max_value

        # Performing element-wise exponentiation
        self.output_matrix = e ** self.output_matrix

        # Performing normalization

        # Adding epsilon to exp_value to avoid division by zero
        exp_value = np.sum(self.output_matrix, axis=1) + epsilon

        # Reshape exp_value to a column vector for broadcasting
        exp_value = np.reshape(exp_value, (-1, 1))

        # Normalize the exponential values by dividing by the sum
        self.output_matrix /= exp_value

    def backward(self, y_true: np.ndarray):

        # Calculating gradients for softmax output

        # Make a copy of self.g_output_matrix to avoid modifying the original matrix
        self.g_softmax_output = self.output_matrix.copy()

        # Subtract 1 from the elements in g_softmax_output corresponding to the true class labels
        self.g_softmax_output[np.arange(len(y_true)), y_true] -= 1


class CrossEntropyLoss:
    def __init__(self):
        self.avg_loss = 0

    def forward(self, y_pre: np.ndarray, y_true: np.ndarray):

        epsilon = 1e-9  # Small value to prevent division by zero

        # Compute the cross-entropy loss
        # Ensure the predicted probability is not zero to avoid log(0)
        probs = np.clip(y_pre[np.arange(len(y_true)), y_true], epsilon, None)

        # Compute the negative log of the predicted probabilities
        cross_entropy_losses = -np.log(probs)

        # Compute the average cross-entropy loss
        self.avg_loss = np.mean(cross_entropy_losses)


class Accuracy:
    def __init__(self):
        self.accuracy = 0

    def forward(self, y_pre: np.ndarray, y_true: np.ndarray):

        # Collect the predicted label index by appending the index of the highest prediction score
        predicted_labels = np.argmax(a=y_pre, axis=1)

        # Compare the predicted labels with the true labels
        correct_count = np.sum(y_true == predicted_labels)

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


def update_weights_and_biases_file():
    np.savez("files/weights&biases_np.npz",
             l1_w=layer1.weights,
             l1_b=layer1.biases,
             l2_w=layer2.weights,
             l2_b=layer2.biases,
             l3_w=layer3.weights,
             l3_b=layer3.biases,
             l4_w=layer4.weights,
             l4_b=layer4.biases,
             l5_w=layer5.weights,
             l5_b=layer5.biases,
             l6_w=layer6.weights,
             l6_b=layer6.biases,
             l7_w=layer7.weights,
             l7_b=layer7.biases,
             )

    print("Weights and biases from all layers were saved!")


# Init =================================================================================================================
init = InitParams()

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

    # Convert lists to NumPy arrays
    X = np.array(X)
    y = np.array(y)

    print(counter)
    forward_loop()
    backward_update_loop()

    if breaker == 3000:
        print("Write 'Exit' to save the weights and biases to file and exit the program")
        print("or write anything else to continue learning without saving")
        user_inp = input(":")
        if user_inp == "Exit":
            update_weights_and_biases_file()
            exit(0)
        else:
            breaker = 0

    counter += 1
    breaker += 1

    # Convert NumPy arrays to list
    X = []
    y = []
