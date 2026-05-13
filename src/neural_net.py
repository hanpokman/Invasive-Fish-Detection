import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import os


class FishClassifier(nn.Module):
    def __init__(self, input_size=1, num_units=32, dropout=0.1):
        super(FishClassifier, self).__init__()

        self.fc1 = nn.Linear(input_size, num_units)
        self.fc2 = nn.Linear(num_units, num_units)
        self.fc3 = nn.Linear(num_units, 1)

        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.sigmoid = nn.Sigmoid()

        self.hyperparams = {
            'input_size': input_size,
            'num_units': num_units,
            'dropout': dropout
        }

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x


def train_model(model, train_lengths, train_labels, hyperparams):
    lr = hyperparams.get('learning_rate', 0.01)
    l2_reg = hyperparams.get('l2_reg', 0.01)
    epochs = hyperparams.get('epochs', 50)
    batch_size = hyperparams.get('batch_size', 16)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=l2_reg)

    X = torch.tensor(train_lengths, dtype=torch.float32).view(-1, 1)
    y = torch.tensor(train_labels, dtype=torch.float32).view(-1, 1)

    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        total_loss = 0.0
        for batch_X, batch_y in loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if epoch % 20 == 0:
            print(f"Epoch {epoch}, Loss: {total_loss / len(loader):.4f}")

    return model


def save_model(model, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    save_dict = {
        'model_state_dict': model.state_dict(),
        'hyperparams': model.hyperparams
    }
    torch.save(save_dict, filepath)


def load_trained_model(filepath, input_size=1, num_units=32, dropout=0.1):
    if os.path.exists(filepath):
        checkpoint = torch.load(filepath)
        if 'hyperparams' in checkpoint:
            hp = checkpoint['hyperparams']
            model = FishClassifier(
                input_size=hp['input_size'],
                num_units=hp['num_units'],
                dropout=hp['dropout']
            )
        else:
            model = FishClassifier(input_size, num_units, dropout)
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model = FishClassifier(input_size, num_units, dropout)
    return model


def predict_species_from_length(model, length_cm, fish_db):
    length_tensor = torch.tensor([[length_cm]], dtype=torch.float32)

    with torch.no_grad():
        output = model(length_tensor)
        probability = output.item()

    candidates = []
    for species, data in fish_db.items():
        avg_len = data.get('avg_length_cm', 20)
        length_diff = abs(length_cm - avg_len) / avg_len
        similarity = 1.0 / (1.0 + length_diff * 3)

        candidates.append({
            'species': species,
            'similarity': similarity,
            'invasive': data.get('invasive', False)
        })

    candidates.sort(key=lambda x: x['similarity'], reverse=True)
    return candidates