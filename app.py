from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# Generate a simple dataset for classification
# The dataset consists of two features (x1, x2) and a binary label (0 or 1)
def generate_classification_data():
    data = []
    labels = []
    for _ in range(100):
        x1 = random.uniform(0, 10)
        x2 = random.uniform(0, 10)
        label = 1 if x1 == x2 else 0  # New decision boundary
        data.append([x1, x2])
        labels.append(label)
    return data, labels

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_dataset', methods=['GET'])
def get_dataset():
    data, labels = generate_classification_data()
    return jsonify({'data': data, 'labels': labels})

@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    num_layers = int(data['layers'])
    problem_type = data['problem']
    input_x1 = float(data['inputX1'])
    input_x2 = float(data['inputX2'])
    learning_rate = float(data['learningRate'])
    activations = data['activations']
    regularizations = data['regularizations']
    regular_rate = float(data['regularRate'])
   
    # More realistic accuracy logic
    if problem_type == 'classification':
        if (input_x1 == input_x2 and random.random() > 0.1):  # Correctly classified
            accuracy = 70 + num_layers * 5 + (1 - learning_rate) * 10
        else:
            accuracy = 30 - num_layers * 5 - (learning_rate) * 10
    else:
        accuracy = 50  # Default accuracy for regression
   
    accuracy = max(min(accuracy, 100), 0)  # Cap accuracy between 0 and 100
   
    # Dummy weights and biases for visualization
    neurons_per_layer = 4  # Fixed neurons per layer for simplicity
    weights = np.random.uniform(-0.1, 0.1, (num_layers, neurons_per_layer)).tolist()
    biases = np.random.uniform(0, 1, num_layers).tolist()

    return jsonify({'accuracy': accuracy, 'layers': num_layers, 'weights': weights, 'biases': biases})

if __name__ == '__main__':
    app.run(debug=True)