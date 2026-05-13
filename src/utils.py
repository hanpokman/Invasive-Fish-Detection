import cv2
import json
import os
import numpy as np


def load_image(path):
    if not os.path.exists(path):
        return None
    img = cv2.imread(path)
    return img


def load_fish_database(db_path):
    default_db = {
        "Bluegill": {"avg_length_cm": 20.0, "invasive": False},
        "Largemouth Bass": {"avg_length_cm": 38.0, "invasive": False},
        "Northern Snakehead": {"avg_length_cm": 45.0, "invasive": True},
        "Lionfish": {"avg_length_cm": 30.0, "invasive": True},
        "Asian Carp": {"avg_length_cm": 70.0, "invasive": True},
        "Rainbow Trout": {"avg_length_cm": 40.0, "invasive": False},
        "Round Goby": {"avg_length_cm": 12.0, "invasive": True},
        "Smallmouth Bass": {"avg_length_cm": 35.0, "invasive": False},
        "Sea Lamprey": {"avg_length_cm": 50.0, "invasive": True}
    }

    if os.path.exists(db_path):
        try:
            with open(db_path, 'r') as f:
                db = json.load(f)
                return db
        except:
            return default_db
    else:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with open(db_path, 'w') as f:
            json.dump(default_db, f, indent=2)
        return default_db