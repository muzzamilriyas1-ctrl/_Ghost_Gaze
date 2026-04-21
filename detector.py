import cv2
import mediapipe as mp
import pygetwindow as gw
import pyautogui
import time
import tkinter as tk
import numpy as np

class GhostGazeDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)
        self.cap = None
        self.owner_profiles = {}
        self.running = False # Control flag

    def get_face_features(self, frame):
        try:
            face_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_img = cv2.resize(face_img, (100, 100))
            return face_img.flatten().astype(np.float32)
        except: return None

    def enroll_owner(self):
        cap = cv2.VideoCapture(0)
        angles = ["FRONT", "LEFT", "RIGHT"]
        captured_data = {}
        for angle in angles:
            while True:
                ret, frame = cap.read()
                if not ret: break
                frame = cv2.flip(frame, 1)
                display = frame.copy()
                cv2.putText(display, f"LOOK {angle} - Press 'C'", (30, 50), 2, 0.8, (0, 255, 0), 2)
                cv2.imshow("Enrollment", display)
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    feat = self.get_face_features(frame)
                    if feat is not None:
                        captured_data[angle] = feat
                        break
        cap.release()
        cv2.destroyAllWindows()
        if len(captured_data) == 3:
            self.owner_profiles = captured_data
            return True
        return False

    def is_privacy_app_active(self, app_list):
        try:
            active_win = gw.getActiveWindowTitle()
            if active_win:
                for app in app_list:
                    if app.lower() in active_win.lower(): return True
        except: return False
        return False

    def show_red_overlay(self, root):
        overlay = tk.Toplevel(root)
        overlay.attributes("-fullscreen", True, "-topmost", True, "-alpha", 0.6)
        overlay.config(bg="red")
        tk.Label(overlay, text="⚠️ STRANGER DETECTED!", font=("Arial", 40, "bold"), fg="white", bg="red").pack(expand=True)
        pyautogui.hotkey('win', 'd') 
        overlay.after(2500, overlay.destroy)

    def start_shield(self, private_apps, threshold, root):
        self.running = True
        print("Sentry Mode: ON")
        while self.running:
            if self.is_privacy_app_active(private_apps):
                if self.cap is None or not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(0)
                
                success, image = self.cap.read()
                if success:
                    image = cv2.flip(image, 1)
                    results = self.face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    if results.detections:
                        if len(results.detections) > 1:
                            root.after(0, lambda: self.show_red_overlay(root))
                            time.sleep(3)
                        else:
                            feat = self.get_face_features(image)
                            if feat is not None:
                                dists = [np.linalg.norm(p - feat) for p in self.owner_profiles.values()]
                                if min(dists) > threshold:
                                    root.after(0, lambda: self.show_red_overlay(root))
                                    time.sleep(3)
            else:
                if self.cap is not None:
                    self.cap.release()
                    self.cap = None
            time.sleep(0.5)
        
        # Cleanup when OFF
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        print("Sentry Mode: OFF")

    def stop_shield(self):
        self.running = False