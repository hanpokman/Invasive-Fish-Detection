# DOUBLE CLICK ME - I'm the main fish spy app!

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
import torch
import json
import os
import sys
from PIL import Image, ImageTk
import threading

# add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# import our modules
from src.stereo_vision import StereoVision
from src.neural_net import FishClassifier, load_trained_model, predict_species_from_length
from src.invasive_detector import InvasiveDetector
from src.utils import load_fish_database


class FishSpyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐟 Invasive Fish Spy Boat - Underwater Detector")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a3a5c')  # ocean blue

        # variables
        self.left_img = None
        self.right_img = None
        self.result = None
        self.detector = None

        # setup UI
        self.setup_ui()

        # load everything in background
        self.load_systems()

    def setup_ui(self):
        # title
        title = tk.Label(self.root, text="🐠 INVASIVE FISH DETECTION SYSTEM 🐡",
                         font=("Arial", 20, "bold"), bg='#1a3a5c', fg='white')
        title.pack(pady=10)

        # subtitle
        subtitle = tk.Label(self.root, text="Underwater Stereo Vision + Neural Network",
                            font=("Arial", 12), bg='#1a3a5c', fg='#aaddff')
        subtitle.pack(pady=5)

        # main frame
        main_frame = tk.Frame(self.root, bg='#1a3a5c')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # left side - images
        images_frame = tk.LabelFrame(main_frame, text="Camera Views", font=("Arial", 12, "bold"),
                                     bg='#2a4a6c', fg='white', padx=10, pady=10)
        images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # left image display
        tk.Label(images_frame, text="Left Camera", bg='#2a4a6c', fg='white').pack()
        self.left_label = tk.Label(images_frame, bg='#0a2a4c', width=40, height=20,
                                   relief=tk.SUNKEN)
        self.left_label.pack(pady=5)

        # right image display
        tk.Label(images_frame, text="Right Camera", bg='#2a4a6c', fg='white').pack()
        self.right_label = tk.Label(images_frame, bg='#0a2a4c', width=40, height=20,
                                    relief=tk.SUNKEN)
        self.right_label.pack(pady=5)

        # right side - controls and results
        controls_frame = tk.LabelFrame(main_frame, text="Control Panel", font=("Arial", 12, "bold"),
                                       bg='#2a4a6c', fg='white', padx=10, pady=10)
        controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

        # buttons
        tk.Button(controls_frame, text="📁 Load Stereo Images", command=self.load_images,
                  font=("Arial", 11), bg='#4a9eff', fg='white', padx=20, pady=5).pack(pady=10)

        tk.Button(controls_frame, text="🔍 Detect Fish!", command=self.detect_fish,
                  font=("Arial", 11, "bold"), bg='#00aa44', fg='white', padx=20, pady=5).pack(pady=10)

        tk.Button(controls_frame, text="🎥 Load Video File", command=self.load_video,
                  font=("Arial", 11), bg='#ff9900', fg='white', padx=20, pady=5).pack(pady=10)

        # status
        self.status_label = tk.Label(controls_frame, text="Status: Loading systems...",
                                     bg='#2a4a6c', fg='yellow', font=("Arial", 10))
        self.status_label.pack(pady=20)

        # results frame
        results_frame = tk.LabelFrame(controls_frame, text="Detection Results",
                                      font=("Arial", 11, "bold"), bg='#2a4a6c', fg='white')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.result_text = tk.Text(results_frame, height=12, width=35, bg='#0a2a4c',
                                   fg='white', font=("Courier", 10))
        self.result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # progress bar
        self.progress = ttk.Progressbar(controls_frame, mode='indeterminate')
        self.progress.pack(pady=10, fill=tk.X)

    def load_systems(self):
        """load models and database in background"""

        def load():
            self.update_status("Loading fish database...")
            self.fish_db = load_fish_database("data/fish_database.json")

            self.update_status("Loading neural network...")
            try:
                self.model = load_trained_model("models/fish_classifier.pth", input_size=1, num_units=32)
            except:
                self.update_status("No trained model found, creating new one...")
                self.model = FishClassifier(input_size=1, num_units=32, dropout=0.1)

            self.update_status("Initializing stereo vision...")
            self.stereo = StereoVision()

            self.update_status("Ready! Load some images to start.")
            self.detector = InvasiveDetector(self.fish_db, self.model, self.stereo)

        thread = threading.Thread(target=load)
        thread.start()

    def update_status(self, msg):
        self.status_label.config(text=f"Status: {msg}")
        self.root.update()

    def load_images(self):
        files = filedialog.askopenfilenames(
            title="Select left and right images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )

        if len(files) >= 2:
            self.left_img = cv2.imread(files[0])
            self.right_img = cv2.imread(files[1])

            # display
            self.display_image(self.left_img, self.left_label)
            self.display_image(self.right_img, self.right_label)

            self.update_status(f"Loaded: {os.path.basename(files[0])} and {os.path.basename(files[1])}")
            self.result_text.insert(tk.END, f"\n📸 Loaded images: {os.path.basename(files[0])}\n")
        elif len(files) == 1:
            # use same image for both
            self.left_img = cv2.imread(files[0])
            self.right_img = self.left_img.copy()
            self.display_image(self.left_img, self.left_label)
            self.display_image(self.right_img, self.right_label)
            self.update_status("Only one image selected, using for both cameras")
        else:
            messagebox.showwarning("No files", "Please select at least 1 image file")

    def display_image(self, img, label):
        # resize for display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (320, 240))
        img_pil = Image.fromarray(img_resized)
        img_tk = ImageTk.PhotoImage(img_pil)
        label.config(image=img_tk)
        label.image = img_tk

    def detect_fish(self):
        if self.left_img is None:
            messagebox.showwarning("No image", "Please load images first!")
            return

        if self.detector is None:
            messagebox.showwarning("Loading", "Systems still loading, please wait...")
            return

        # start progress bar
        self.progress.start()
        self.update_status("Detecting fish...")

        def detect():
            try:
                # run detection
                result = self.detector.detect(self.left_img, self.right_img)
                self.result = result

                # update UI in main thread
                self.root.after(0, self.show_results, result)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.update_status("Detection complete"))

        thread = threading.Thread(target=detect)
        thread.start()

    def show_results(self, result):
        self.result_text.delete(1.0, tk.END)

        # big title
        if result['invasive']:
            self.result_text.insert(tk.END, "⚠️⚠️⚠️ INVASIVE SPECIES DETECTED! ⚠️⚠️⚠️\n", "invasive")
            self.result_text.tag_config("invasive", foreground="red", font=("Arial", 12, "bold"))
        else:
            self.result_text.insert(tk.END, "✅ NATIVE FISH DETECTED ✅\n", "native")
            self.result_text.tag_config("native", foreground="lightgreen", font=("Arial", 12, "bold"))

        self.result_text.insert(tk.END, "\n" + "=" * 35 + "\n")
        self.result_text.insert(tk.END, f"🐟 Species: {result['species']}\n")
        self.result_text.insert(tk.END, f"📏 Length: {result['length_cm']:.1f} cm\n")
        self.result_text.insert(tk.END, f"🎯 Confidence: {result['confidence']:.2%}\n")

        if result['invasive']:
            self.result_text.insert(tk.END, f"🚨 ACTION: Report to authorities!\n")
        else:
            self.result_text.insert(tk.END, f"🌊 Status: Protected native species\n")

        self.result_text.insert(tk.END, "\n" + "=" * 35 + "\n")
        self.result_text.insert(tk.END, "Top candidates:\n")
        for i, cand in enumerate(result.get('top_candidates', [])[:3]):
            marker = "🚨" if cand['invasive'] else "✅"
            self.result_text.insert(tk.END, f"  {i + 1}. {marker} {cand['species']} ({cand['similarity']:.2%})\n")

    def load_video(self):
        filepath = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )

        if filepath:
            self.update_status("Opening video...")
            # open video in new window
            video_window = tk.Toplevel(self.root)
            video_window.title("Video Detection")
            video_window.geometry("800x600")

            label = tk.Label(video_window)
            label.pack()

            cap = cv2.VideoCapture(filepath)

            def process_video():
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # use frame for both cameras
                    result = self.detector.detect(frame, frame)

                    # draw results on frame
                    color = (0, 0, 255) if result['invasive'] else (0, 255, 0)
                    text = f"{result['species']} | {result['length_cm']:.1f}cm"
                    if result['invasive']:
                        text += " | INVASIVE!"
                    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                    # convert for tkinter
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_resized = cv2.resize(frame_rgb, (780, 540))
                    img_pil = Image.fromarray(frame_resized)
                    img_tk = ImageTk.PhotoImage(img_pil)

                    label.config(image=img_tk)
                    label.image = img_tk

                    video_window.update()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                cap.release()

            thread = threading.Thread(target=process_video)
            thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = FishSpyApp(root)
    root.mainloop()