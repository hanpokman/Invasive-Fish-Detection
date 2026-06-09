
# 🐟 Invasive Fish Spy Boat - Underwater Detection System

**⚠️ RECONSTRUCTION NOTICE ⚠️**

This code is a **reconstruction** of a project originally built in 2023. The original code, along with months of underwater footage and trained model weights, was lost when a 2TB external hard drive failed catastrophically (RIP 2019-2024, you served us well). 

What you see here is a rebuild from memory, scattered notes, and some old screenshots. The core logic remains the same, but the original datasets and production-trained models are gone forever. Consider this a **functional replica** rather than the original masterpiece.

---

## 🔬 Part of Our ISEF Project

This repository contains **one function** of our larger International Science and Engineering Fair (ISEF) project: "Autonomous Ecosystem Surveillance Robot"

Full Project Links:
Addl. Info: https://isef.net/project/enev002t-autonomous-ecosystem-surveillance-vehicle
Research Poster: https://drive.google.com/file/d/1x2lOwrA_mzi1pvO8K9LVGTb7Tlk-M5DN/view?usp=sharing

Other components of our ISEF project (not in this repo):
- Autonomous boat navigation system (Raspberry PI+ GPS + on-off shore communication)
- Edge deployment on Raspberry Pi with Coral TPU
- Water quality sensors integrated with fish detection

This repo focuses **only** on the computer vision + neural network inference pipeline. The full system integration docs are available at the links above.

---

## 📖 The Original Project (2023)

Back in 2023, as part of our ISEF submission, we built an autonomous boat that used stereo cameras mounted on a lowering platform to survey underwater ecosystems. The idea was simple: instead of relying on clear, well-lit images (which you rarely get underwater), the system focused on the **silhouette** of the fish - which is way more reliable in murky waters.

**How it worked**

1. Boat lowers camera platform underwater
2. Stereo vision calculates fish length from the silhouette
3. Length gets fed into a 4-layer neural network: (derived from hyperparameter searching)
   - 2 hidden layers (32 units each)
   - Dropout: 0.1
   - L2 regularization: 0.01
   - Learning rate: 0.01
   - Optimizer: Adam
   - Output: Sigmoid (invasive vs native probability)
4. Model spits out possible fish species based on length
5. Image similarity model (not included in this repo - proprietary) compares against my pre-uploaded local fish database
6. **RESULT:** Invasive? Native? You know immediately

---

```


**DISTRIBUTION OF DATASET**

<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics (5)" src="https://github.com/user-attachments/assets/110b1e9d-c55d-4099-8900-fec8ae155cb6" />


<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics (6)" src="https://github.com/user-attachments/assets/7d57eecb-8146-4dbc-b3ca-1a031ca3a948" />

<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics (7)" src="https://github.com/user-attachments/assets/12661f2f-8291-4a2a-ace7-b46b4a637287" />
---

## 🚀 Getting Started (Reconstruction Version)

Since the original models are gone, you'll need to train new ones. The code is set up to work with any fish dataset you provide.

### 1. Install dependencies (double-click)
```bash
run_me_first.py
```

### 2. Create the fish database
```bash
create_database.py
```

### 3. Train a new model (use your own data or the dummy data)
```bash
train_simple.py
```

### 4. Launch the GUI
```bash
main_app.py
```

### 5. Quick test with fake fish
```bash
quick_test.py
```

---

## 📊 What You Can Do With This

- **Load stereo images** (left/right camera pairs) and get fish measurements
- **Run inference** through the neural network to classify invasive vs native
- **Process video files** frame-by-frame
- **Export detection logs** (coming soon)

The original boat used a Raspberry Pi 4 + Coral USB accelerator for edge inference. The stereo cameras were two Logitech C920s modified with underwater housings. Worked surprisingly well until a seal failed at 3 meters and flooded the electronics bay (different failure, not the hard drive one).

---

## 🧠 Neural Network Architecture

```
Input Layer: 1 node (fish length in cm)
    ↓
Hidden Layer 1: 32 nodes + ReLU + Dropout(0.1)
    ↓
Hidden Layer 2: 32 nodes + ReLU + Dropout(0.1)
    ↓
Output Layer: 1 node + Sigmoid (probability invasive)
```

**Why this architecture?** Because it worked. We tried 64 units, 128 units, 3 hidden layers, no dropout, different activations... this combo gave 89% validation accuracy on the original dataset while being small enough to run on the boat's limited hardware. This was a key requirement for ISEF - efficient edge deployment.

---

## 📁 Project Structure (Reconstructed)

```
invasive-fish-spy/
├── run_me_first.py          # Install dependencies
├── create_database.py       # Build fish database
├── train_simple.py          # Train neural network
├── main_app.py              # GUI application
├── quick_test.py            # Test with fake images
├── src/                     # Core modules
│   ├── stereo_vision.py     # Length measurement
│   ├── neural_net.py        # The 4-layer network
│   ├── invasive_detector.py # Detection pipeline
│   └── utils.py             # Helpers
├── data/                    # Sample fish database
└── models/                  # Trained models (auto-created)

```

---

## 🔬 Hyperparameter Testing Results
Pipeline

<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics" src="https://github.com/user-attachments/assets/834ca77c-5397-4819-b53b-c88576e8d5e5" />

Testing different proportions of dataset splitting

<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics (2)" src="https://github.com/user-attachments/assets/91543baa-6cb8-4932-8d9e-358b798724bf" />

Initial Training Curve

<img width="387" height="348" alt="Screenshot 2026-05-14 at 12 43 11 AM" src="https://github.com/user-attachments/assets/13a8ebaf-3afd-49c8-9bf3-765f23c0b686" />

Results of Hyperparameter Searching

<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics (3)" src="https://github.com/user-attachments/assets/abca6bcf-2815-4e7b-9bb2-d4bdabe97f53" />

Improved Results

<img width="960" height="540" alt="Fish Species Classification based on Fish Characteristics (4)" src="https://github.com/user-attachments/assets/4a9edd36-69eb-464a-b14f-4955241df8bf" />




---
