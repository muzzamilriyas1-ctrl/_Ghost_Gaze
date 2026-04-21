import tkinter as tk
from tkinter import messagebox
from detector import GhostGazeDetector
from config import PRIVATE_APPS, FACE_MATCH_THRESHOLD
import threading

class GhostGazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GhostGaze AI")
        self.root.geometry("400x450")
        self.root.configure(bg="#121212")
        self.detector = GhostGazeDetector()

        tk.Label(root, text="GHOSTGAZE", font=("Impact", 45), fg="#ff3e3e", bg="#121212").pack(pady=30)
        
        self.status = tk.Label(root, text="STATUS: STANDBY", fg="#7f8c8d", bg="#121212", font=("Arial", 10, "bold"))
        self.status.pack()

        tk.Button(root, text="1. ENROLL OWNER", command=self.enroll, bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=25, height=2).pack(pady=10)
        
        # Combined Toggle Button
        self.toggle_btn = tk.Button(root, text="2. START SENTRY", command=self.toggle_sentry, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=25, height=2, state="disabled")
        self.toggle_btn.pack(pady=10)

    def enroll(self):
        if self.detector.enroll_owner():
            self.status.config(text="STATUS: OWNER READY", fg="#2ecc71")
            self.toggle_btn.config(state="normal")
            messagebox.showinfo("GhostGaze", "Enrollment Successful!")

    def toggle_sentry(self):
        if not self.detector.running:
            # START logic
            self.toggle_btn.config(text="STOP SENTRY", bg="#e74c3c")
            self.status.config(text="STATUS: SHIELD ACTIVE", fg="#2ecc71")
            threading.Thread(target=self.detector.start_shield, args=(PRIVATE_APPS, FACE_MATCH_THRESHOLD, self.root), daemon=True).start()
        else:
            # STOP logic
            self.detector.stop_shield()
            self.toggle_btn.config(text="START SENTRY", bg="#2ecc71")
            self.status.config(text="STATUS: OWNER READY", fg="#7f8c8d")
            messagebox.showinfo("GhostGaze", "Sentry Mode Deactivated.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GhostGazeApp(root)
    root.mainloop()