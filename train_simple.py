# DOUBLE CLICK ME - trains the fish neural network

import torch
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.neural_net import FishClassifier, train_model, save_model

print("🐟 TRAINING FISH NEURAL NETWORK 🐟")
print("="*50)

# create training data (lengths and invasive status)
print("Creating training data...")
np.random.seed(42)

train_lengths = []
train_labels = []

# native fish (smaller, 15-30 cm)
for i in range(150):
    length = np.random.normal(23, 6)
    train_lengths.append(max(5, min(50, length)))
    train_labels.append(0)  # native

# invasive fish (larger, 30-60 cm)
for i in range(150):
    length = np.random.normal(42, 10)
    train_lengths.append(max(15, min(80, length)))
    train_labels.append(1)  # invasive

# mix them up
indices = np.random.permutation(len(train_lengths))
train_lengths = np.array(train_lengths)[indices]
train_labels = np.array(train_labels)[indices]

print(f"Training samples: {len(train_lengths)}")
print(f"Native: {sum(1 for x in train_labels if x==0)}")
print(f"Invasive: {sum(1 for x in train_labels if x==1)}")

# hyperparameters (your specs!)
hyperparams = {
    'learning_rate': 0.01,
    'l2_reg': 0.01,
    'epochs': 100,
    'batch_size': 16
}

print(f"\nHyperparameters:")
print(f"  Learning rate: {hyperparams['learning_rate']}")
print(f"  L2 Regularization: {hyperparams['l2_reg']}")
print(f"  Epochs: {hyperparams['epochs']}")
print(f"  Batch size: {hyperparams['batch_size']}")

# create model
print("\nCreating neural network...")
model = FishClassifier(
    input_size=1,   # just length
    num_units=32,   # 32 neurons per hidden layer
    dropout=0.1     # dropout rate
)

print(f"Network architecture:")
print(f"  Input layer: 1 node")
print(f"  Hidden layer 1: 32 nodes")
print(f"  Hidden layer 2: 32 nodes")
print(f"  Output layer: 1 node (sigmoid)")

# train
print("\nTraining (this might take a minute)...")
print("-" * 50)
trained_model = train_model(model, train_lengths, train_labels, hyperparams)

# save model
os.makedirs("models", exist_ok=True)
save_model(trained_model, "models/fish_classifier.pth")

print("\n" + "="*50)
print("✅ TRAINING COMPLETE!")
print("="*50)

# test the model
print("\nQuick test on sample lengths:")
test_lengths = [15, 25, 35, 45, 55, 65]
for length in test_lengths:
    with torch.no_grad():
        pred = trained_model(torch.tensor([[float(length)]]))
        prob = pred.item()
        verdict = "🚨 INVASIVE" if prob > 0.5 else "✅ NATIVE"
        print(f"  {length} cm: {prob:.2%} chance invasive -> {verdict}")

print("\n💾 Model saved to: models/fish_classifier.pth")
input("\nPress Enter to exit...")