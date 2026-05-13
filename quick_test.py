# DOUBLE CLICK ME - automatic test without any images!

import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🐟 FISH SPY BOAT - QUICK TEST MODE 🐟")
print("="*50)

# create fake images
print("Creating fake underwater images...")
fake_fish = np.zeros((480, 640, 3), dtype=np.uint8)
# draw a fake fish shape
cv2.ellipse(fake_fish, (320, 240), (80, 30), 0, 0, 360, (255,255,255), -1)
cv2.ellipse(fake_fish, (260, 230), (20, 20), 0, 0, 360, (0,0,0), -1)  # eye
cv2.putText(fake_fish, "FAKE FISH", (250, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

# save temp images
cv2.imwrite("temp_left.jpg", fake_fish)
cv2.imwrite("temp_right.jpg", fake_fish)

print("Loading modules...")

from src.stereo_vision import StereoVision
from src.neural_net import FishClassifier, load_trained_model
from src.invasive_detector import InvasiveDetector
from src.utils import load_fish_database

print("Loading database...")
fish_db = load_fish_database("data/fish_database.json")

print("Loading model...")
try:
    model = load_trained_model("models/fish_classifier.pth")
except:
    print("No model found, creating new untrained model")
    model = FishClassifier()

print("Initializing detector...")
stereo = StereoVision()
detector = InvasiveDetector(fish_db, model, stereo)

print("Running detection on fake fish...")
left = cv2.imread("temp_left.jpg")
right = cv2.imread("temp_right.jpg")

result = detector.detect(left, right)

print("\n" + "="*50)
print("RESULTS:")
print("="*50)
print(f"Species: {result['species']}")
print(f"Length: {result['length_cm']:.2f} cm")
print(f"Invasive: {result['invasive']}")
print(f"Confidence: {result['confidence']:.2%}")
print("="*50)

# cleanup
os.remove("temp_left.jpg")
os.remove("temp_right.jpg")

input("\nPress Enter to exit...")