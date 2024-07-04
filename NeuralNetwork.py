import numpy as np

class NeuralNetwork:
    def __init__(self):
        self.weights_input_hidden = np.random.randn(7, 10)
        self.weights_hidden_output = np.random.randn(10, 1)
    
    def forward(self, inputs):
        hidden = np.dot(inputs, self.weights_input_hidden)
        hidden = self.sigmoid(hidden)
        output = np.dot(hidden, self.weights_hidden_output)
        output = self.sigmoid(output)
        return output

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
