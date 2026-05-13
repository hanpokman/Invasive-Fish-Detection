import cv2
import numpy as np
import os
import json


class StereoVision:
    def __init__(self, calibration_dir=None):
        self.baseline_cm = 12.0
        self.focal_length_px = 700.0
        self.pixel_to_cm_ratio = 0.045

        if calibration_dir and os.path.exists(calibration_dir):
            self.load_calibration(calibration_dir)

    def load_calibration(self, calib_dir):
        left_file = os.path.join(calib_dir, "left_camera.yaml")
        if os.path.exists(left_file):
            try:
                with open(left_file, 'r') as f:
                    calib = json.load(f)
                    self.focal_length_px = calib.get('focal_length', 700)
            except:
                pass

    def find_fish_contour(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # adaptive threshold for silhouette
        thresh = cv2.adaptiveThreshold(blurred, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None

        largest = max(contours, key=cv2.contourArea)
        return largest

    def measure_fish_length(self, left_img, right_img):
        contour = self.find_fish_contour(left_img)

        if contour is None:
            return 15.0  # default guess if no fish found

        x, y, w, h = cv2.boundingRect(contour)
        pixel_length = max(w, h)
        real_length_cm = pixel_length * self.pixel_to_cm_ratio
        real_length_cm = max(real_length_cm, 5.0)  # at least 5cm

        return real_length_cm

    def get_disparity_map(self, left_img, right_img):
        gray_left = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
        stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
        disparity = stereo.compute(gray_left, gray_right)
        return disparity