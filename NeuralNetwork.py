import numpy as np
from dinoAIParallel import KeyClassifier

class KeyNNClassifier(KeyClassifier):
    def __init__(self, state):
        super().__init__(state)
        self.state = state
        self.model = self.build_model()

    def build_model(self):
        model = {
            'W1': np.random.randn(7, 128) * 0.01,
            'b1': np.zeros((1, 128)),
            'W2': np.random.randn(128, 128) * 0.01,
            'b2': np.zeros((1, 128)),
            'W3': np.random.randn(128, 128) * 0.01,
            'b3': np.zeros((1, 128)),
            'W4': np.random.randn(128, 3) * 0.01,
            'b4': np.zeros((1, 3))
        }
        return model

    def relu(self, Z):
        return np.maximum(0, Z)

    def softmax(self, Z):
        expZ = np.exp(Z - np.max(Z))
        return expZ / expZ.sum(axis=1, keepdims=True)

    def forward_propagation(self, X):
        model = self.model

        model['Z1'] = np.dot(X, model['W1']) + model['b1']
        model['A1'] = self.relu(model['Z1'])
        model['Z2'] = np.dot(model['A1'], model['W2']) + model['b2']
        model['A2'] = self.relu(model['Z2'])
        model['Z3'] = np.dot(model['A2'], model['W3']) + model['b3']
        model['A3'] = self.relu(model['Z3'])
        model['Z4'] = np.dot(model['A3'], model['W4']) + model['b4']
        model['A4'] = self.softmax(model['Z4'])

        return model['A4']

    def train_model(self, X_train, y_train, epochs=50, learning_rate=0.001):
        m = X_train.shape[0]

        for epoch in range(epochs):
            A4 = self.forward_propagation(X_train)

            # One-hot encoding dos rótulos
            y_one_hot = np.eye(3)[y_train]

            # Backpropagation
            dZ4 = A4 - y_one_hot
            dW4 = np.dot(self.model['A3'].T, dZ4) / m
            db4 = np.sum(dZ4, axis=0, keepdims=True) / m

            dA3 = np.dot(dZ4, self.model['W4'].T)
            dZ3 = dA3 * (self.model['A3'] > 0)
            dW3 = np.dot(self.model['A2'].T, dZ3) / m
            db3 = np.sum(dZ3, axis=0, keepdims=True) / m

            dA2 = np.dot(dZ3, self.model['W3'].T)
            dZ2 = dA2 * (self.model['A2'] > 0)
            dW2 = np.dot(self.model['A1'].T, dZ2) / m
            db2 = np.sum(dZ2, axis=0, keepdims=True) / m

            dA1 = np.dot(dZ2, self.model['W2'].T)
            dZ1 = dA1 * (self.model['A1'] > 0)
            dW1 = np.dot(X_train.T, dZ1) / m
            db1 = np.sum(dZ1, axis=0, keepdims=True) / m

            # Atualização dos parâmetros
            self.model['W4'] -= learning_rate * dW4
            self.model['b4'] -= learning_rate * db4
            self.model['W3'] -= learning_rate * dW3
            self.model['b3'] -= learning_rate * db3
            self.model['W2'] -= learning_rate * dW2
            self.model['b2'] -= learning_rate * db2
            self.model['W1'] -= learning_rate * dW1
            self.model['b1'] -= learning_rate * db1

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        obType_encoded = 1 if isinstance(obType, Bird) else 0
        nextObType_encoded = 1 if isinstance(nextObType, Bird) else 0
        input_data = np.array([[distance, obHeight, speed, obType_encoded, nextObDistance, nextObHeight, nextObType_encoded]])
        predictions = self.forward_propagation(input_data)
        action = np.argmax(predictions)

        if action == 0:
            return "K_NO"
        elif action == 1:
            return "K_UP"
        elif action == 2:
            return "K_DOWN"