import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# File to store fitness data
DATA_FILE = "fitness_data.json"

# Constants for calculations
CALORIES_PER_STEP = 0.04  # Approximate calories burned per step
STRIDE_LENGTH = 0.75      # Average stride length in meters

class FitnessTracker:
    def __init__(self):
        self.user_data = self.load_data()
        self.today = datetime.now().strftime("%Y-%m-%d")
        if self.today not in self.user_data:
            self.user_data[self.today] = {"steps": 0, "weight": None}

    def load_data(self):
        """Load existing fitness data from file or create a new one."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_data(self):
        """Save fitness data to file."""
        with open(DATA_FILE, "w") as file:
            json.dump(self.user_data, file, indent=4)

    def set_weight(self, weight):
        """Set user's weight for calorie calculation."""
        self.user_data[self.today]["weight"] = weight
        self.save_data()
        return f"Weight set to {weight} kg."

    def add_steps(self, steps):
        """Add steps to today's count."""
        self.user_data[self.today]["steps"] += steps
        self.save_data()
        return f"Added {steps} steps. Total today: {self.user_data[self.today]['steps']}"

    def calculate_calories(self):
        """Calculate calories burned based on steps and weight."""
        if self.user_data[self.today]["weight"] is None:
            return "Please set your weight first."
        steps = self.user_data[self.today]["steps"]
        calories = steps * CALORIES_PER_STEP * self.user_data[self.today]["weight"] / 70
        return round(calories, 2)

    def calculate_distance(self):
        """Calculate distance covered in kilometers."""
        steps = self.user_data[self.today]["steps"]
        distance = (steps * STRIDE_LENGTH) / 1000  # Convert meters to kilometers
        return round(distance, 2)

    def get_summary(self):
        """Return today's fitness summary as a string."""
        steps = self.user_data[self.today]["steps"]
        calories = self.calculate_calories()
        distance = self.calculate_distance()
        
        summary = f"--- Fitness Summary for {self.today} ---\n"
        summary += f"Steps Taken: {steps}\n"
        summary += f"Distance Covered: {distance} km\n"
        if isinstance(calories, str):
            summary += calories
        else:
            summary += f"Calories Burned: {calories} kcal"
        return summary

    def reset_data(self):
        """Reset all data to factory settings."""
        self.user_data.clear()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.user_data[self.today] = {"steps": 0, "weight": None}
        self.save_data()
        return "All data reset to factory settings."

class FitnessApp:
    def __init__(self, root):
        self.tracker = FitnessTracker()
        self.root = root
        self.root.title("Personal Fitness Tracker (P3)")
        self.root.geometry("400x600")

        # Main Canvas for background and widgets
        self.main_frame = tk.Canvas(root, bg="#f0f4f8", highlightthickness=0)
        self.main_frame.pack(expand=True, fill="both")

        # Load and set background image
        try:
            image_path = "/Users/hemanthkunta/Downloads/project/fintness tracker/fitness_background.png"
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found at: {image_path}")
            image = Image.open(image_path)
            image = image.resize((400, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.main_frame.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.main_frame.configure(bg="#f0f4f8")

        # Header
        self.header_label = tk.Label(self.main_frame, text="Fitness Tracker", 
                                     font=("Helvetica", 20, "bold"), 
                                     bg="#4a90e2", fg="white", pady=10, padx=20)
        self.header = self.main_frame.create_window(200, 30, window=self.header_label, anchor="center")

        # Weight Entry
        self.weight_label = tk.Label(self.main_frame, text="Enter Weight (kg):", 
                                     font=("Helvetica", 14, "bold"), 
                                     fg="black", bg="gray15")
        self.main_frame.create_window(200, 100, window=self.weight_label, anchor="center")

        self.weight_entry = tk.Entry(self.main_frame, font=("Helvetica", 12), fg="white", bg="gray15")
        self.main_frame.create_window(200, 130, window=self.weight_entry, anchor="center")

        # Button: Set Weight - Transparent with visible black text
        self.weight_button = tk.Button(self.main_frame, text="Set Weight", 
                                       command=self.set_weight, 
                                       font=("Helvetica", 12, "bold"), 
                                       bg="gray15", fg="black", 
                                       activebackground="gray25", activeforeground="yellow", 
                                       borderwidth=1, relief="flat")
        self.main_frame.create_window(200, 170, window=self.weight_button, anchor="center")

        # Steps Entry
        self.steps_label = tk.Label(self.main_frame, text="Enter Steps:", 
                                    font=("Helvetica", 14, "bold"), 
                                    fg="black", bg="gray15")
        self.main_frame.create_window(200, 210, window=self.steps_label, anchor="center")

        self.steps_entry = tk.Entry(self.main_frame, font=("Helvetica", 12), fg="white", bg="gray15")
        self.main_frame.create_window(200, 240, window=self.steps_entry, anchor="center")

        # Button: Add Steps - Transparent with visible black text
        self.steps_button = tk.Button(self.main_frame, text="Add Steps", 
                                      command=self.add_steps, 
                                      font=("Helvetica", 12, "bold"), 
                                      bg="gray15", fg="black", 
                                      activebackground="gray25", activeforeground="yellow", 
                                      borderwidth=1, relief="flat")
        self.main_frame.create_window(200, 280, window=self.steps_button, anchor="center")

        # Button: Show Summary - Transparent with visible green text
        self.summary_button = tk.Button(self.main_frame, text="Show Summary", 
                                        command=self.show_summary, 
                                        font=("Helvetica", 12, "bold"), 
                                        bg="gray15", fg="#00ff00", 
                                        activebackground="gray25", activeforeground="yellow", 
                                        borderwidth=1, relief="flat")
        self.main_frame.create_window(200, 320, window=self.summary_button, anchor="center")

        # Result Display - Transparent with visible white text
        self.result_label = tk.Label(self.main_frame, text="", font=("Helvetica", 12), 
                                     bg="gray15", fg="white", justify="left", width=30, height=5)
        self.main_frame.create_window(200, 400, window=self.result_label, anchor="center")

        # Button: Clear - Transparent with visible black text
        self.clear_button = tk.Button(self.main_frame, text="Clear", 
                                      command=self.clear_data, 
                                      font=("Helvetica", 12, "bold"), 
                                      bg="gray15", fg="black", 
                                      activebackground="gray25", activeforeground="yellow", 
                                      borderwidth=1, relief="flat")
        self.main_frame.create_window(200, 460, window=self.clear_button, anchor="center")

        # Button: Reset All Data - Transparent with visible red text
        self.reset_button = tk.Button(self.main_frame, text="Reset All Data", 
                                      command=self.reset_data, 
                                      font=("Helvetica", 12, "bold"), 
                                      bg="gray15", fg="#ff4444", 
                                      activebackground="gray25", activeforeground="yellow", 
                                      borderwidth=1, relief="flat")
        self.main_frame.create_window(200, 500, window=self.reset_button, anchor="center")

        # Button: Exit - Transparent with visible black text
        self.exit_button = tk.Button(self.main_frame, text="Exit", 
                                     command=root.quit, 
                                     font=("Helvetica", 12, "bold"), 
                                     bg="gray15", fg="black", 
                                     activebackground="gray25", activeforeground="yellow", 
                                     borderwidth=1, relief="flat")
        self.main_frame.create_window(200, 540, window=self.exit_button, anchor="center")

    def set_weight(self):
        try:
            weight = float(self.weight_entry.get())
            if weight <= 0:
                messagebox.showerror("Error", "Weight must be positive.")
            else:
                result = self.tracker.set_weight(weight)
                self.result_label.config(text=result)
                self.weight_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for weight.")

    def add_steps(self):
        try:
            steps = int(self.steps_entry.get())
            if steps < 0:
                messagebox.showerror("Error", "Steps cannot be negative.")
            else:
                result = self.tracker.add_steps(steps)
                self.result_label.config(text=result)
                self.steps_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for steps.")

    def show_summary(self):
        summary = self.tracker.get_summary()
        self.result_label.config(text=summary)

    def clear_data(self):
        """Clear all data from the entries and result label."""
        self.weight_entry.delete(0, tk.END)
        self.steps_entry.delete(0, tk.END)
        self.result_label.config(text="")

    def reset_data(self):
        """Reset all data and update the UI."""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all data? This cannot be undone."):
            result = self.tracker.reset_data()
            self.result_label.config(text=result)
            self.weight_entry.delete(0, tk.END)
            self.steps_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessApp(root)
    root.mainloop()