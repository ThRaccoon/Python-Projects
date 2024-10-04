# ==================================================
#  Test Script: GPU Implementation (CuPy v12.4)
# ==================================================
# This script tests the neural network using CuPy
# (v12.4) for GPU-based computations. It validates
# the performance and speed improvements with
# CUDA support.
# ==================================================


import ast
import cupy as cp


# Classes ==============================================================================================================
class LayerDense:
    instance_counter = 1

    def __init__(self, n_inputs: int, n_neurons: int):
        # Forward
        self.weights = cp.empty((0, 0))
        self.biases = cp.empty(0)
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons
        self.output_matrix = cp.empty((0, 0))

        # Instance counter
        self.id = LayerDense.instance_counter
        LayerDense.instance_counter += 1

        try:
            self.read_weights_and_biases_from_file()
            print(f"Weights and biases for L{self.id} were loaded from a file!")
        except (FileNotFoundError, EOFError):
            print(f"L{self.id} Weights and biases are missing from the file or the file is missing!")

    def forward(self, input_matrix: cp.ndarray):

        # Computes the output of the neural network by performing a matrix multiplication
        # of the input matrix with the weights and adding biases
        self.output_matrix = cp.dot(input_matrix, self.weights) + self.biases

    def read_weights_and_biases_from_file(self):
        with cp.load("../gpu_training/files/weights&biases_cp.npz") as _file:
            self.weights = _file[f"l{self.id}_w"]
            self.biases = _file[f"l{self.id}_b"]


class ActivationReLU:
    def __init__(self):
        # Forward
        self.input_matrix = cp.empty((0, 0))
        self.output_matrix = cp.empty((0, 0))

    def forward(self, input_matrix: cp.ndarray):
        # Applying the ReLU function to each element of the input_matrix

        # Saving the input matrix for later use (in backpropagation)
        self.input_matrix = input_matrix

        # Applying the ReLU function to each element of the input_matrix
        self.output_matrix = cp.maximum(0, input_matrix)


class ActivationSoftmax:
    def __init__(self):
        # Forward
        self.output_matrix = cp.empty((0, 0))

    def forward(self, input_matrix: cp.ndarray):
        # Applying the Softmax function to each element of the input_matrix

        # Euler number
        e = 2.7182818
        epsilon = 1e-9  # Small value to prevent division by zero
        self.output_matrix = cp.empty((0, 0))

        # Subtracting the max value of each row to prevent overflow
        max_value = cp.max(input_matrix, axis=1)

        # Reshape it to make it column vector
        max_value = cp.reshape(max_value, (-1, 1))

        self.output_matrix = input_matrix - max_value

        # Performing element-wise exponentiation
        self.output_matrix = e ** self.output_matrix

        # Performing normalization

        # Adding epsilon to exp_value to avoid division by zero
        exp_value = cp.sum(self.output_matrix, axis=1) + epsilon

        # Reshape exp_value to a column vector for broadcasting
        exp_value = cp.reshape(exp_value, (-1, 1))

        # Normalize the exponential values by dividing by the sum
        self.output_matrix /= exp_value


class CrossEntropyLoss:
    def __init__(self):
        self.avg_loss = 0

    def forward(self, y_pre: cp.ndarray, y_true: cp.ndarray):
        epsilon = 1e-9

        # Compute the cross-entropy loss
        # Ensure the predicted probability is not zero to avoid log(0)
        probs = cp.clip(y_pre[cp.arange(len(y_true)), y_true], epsilon, None)

        # Compute the negative log of the predicted probabilities
        cross_entropy_losses = -cp.log(probs)

        # Compute the average cross-entropy loss
        self.avg_loss = cp.mean(cross_entropy_losses)


class Accuracy:
    def __init__(self):
        self.accuracy = 0

    def forward(self, y_pre: cp.ndarray, y_true: cp.ndarray):
        # Collect the predicted label index by appending the index of the highest prediction score
        predicted_labels = cp.argmax(a=y_pre, axis=1)

        # Compare the predicted labels with the true labels
        correct_count = cp.sum(y_true == predicted_labels)

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


# Init =================================================================================================================
# Learning rate
lr = 0.0005

# Lambda strength (L2 regularization strength)
lambda_str = 0.001


# Neural network architecture ==========================================================================================
layer1 = LayerDense(784, 512)
relu1 = ActivationReLU()

layer2 = LayerDense(512, 256)
relu2 = ActivationReLU()

layer3 = LayerDense(256, 128)
relu3 = ActivationReLU()

layer4 = LayerDense(128, 64)
relu4 = ActivationReLU()

layer5 = LayerDense(64, 32)
relu5 = ActivationReLU()

layer6 = LayerDense(32, 16)
relu6 = ActivationReLU()

layer7 = LayerDense(16, 10)
softmax1 = ActivationSoftmax()

loss = CrossEntropyLoss()
accuracy = Accuracy()


# Testing ==============================================================================================================
X = []
y = []
file_lines = []
with open("../training&testing_data/formatted_testing_data.csv", "r") as file:
    for line in file:
        file_lines.append(ast.literal_eval(line.strip()))

for i in range(len(file_lines)):
    temp = file_lines[i]
    X.append(temp[:-1])
    y.append(temp[-1])

    # Convert lists to CuPy arrays
    X = cp.array(X)
    y = cp.array(y)

    forward_loop()
    predicted_label = cp.argmax(softmax1.output_matrix)

    print(f"True label:      '{y[0]}'")
    print(f"Predicted label: '{predicted_label}'")
    print()

    # Convert CuPy arrays back to list
    X = []
    y = []
