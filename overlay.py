import cv2
import numpy as np

def draw_overlay(frame):
    overlay = np.zeros_like(frame)
    cv2.putText(overlay, "PRIVACY SHIELD ACTIVE", (80, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    cv2.putText(overlay, "Stranger Detected!", (160, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    return overlay

def draw_status(frame, privacy_on, face_count):
    color = (0, 0, 255) if privacy_on else (0, 255, 0)
    status = "PRIVACY: ON" if privacy_on else "PRIVACY: OFF"
    cv2.putText(frame, status, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(frame, f"Faces: {face_count}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    return frame
import tkinter as tk

def show_privacy_alert():
    alert = tk.Toplevel()
    alert.attributes("-fullscreen", True)
    alert.attributes("-alpha", 0.6) # 60% transparent
    alert.bg = "red"
    alert.configure(bg="red")
    
    label = tk.Label(alert, text="⚠️ PRIVACY BREACH DETECTED!", 
                     font=("Arial", 40, "bold"), fg="white", bg="red")
    label.pack(expand=True)
    
    # 3 seconds aprom alert close aagum
    alert.after(3000, alert.destroy)