import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white", height=10000, padx=10, pady=10)
        image = Image.open("hospital.jpeg")
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self, image=photo)
        image_label.image = photo 
        image_label.place(relwidth=1, relheight=1)
        title_label = tk.Label(self, text="Welcome to Meditrack App", font=("Helvetica", 60, "bold"), fg="white")
        title_label.pack(pady=40)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=80)
        patient_button = tk.Button(button_frame, text="I'm a Patient", command=self.patient_login)
        nurse_button = tk.Button(button_frame, text="I'm a Nurse", command=self.nurse_login)
        doctor_button = tk.Button(button_frame, text="I'm a Doctor", command=self.doctor_login)
        admin_button = tk.Button(button_frame, text="I'm an Admin", command=self.admin_login)
        patient_button.pack(side="left", fill="both", expand=True, padx=10)
        nurse_button.pack(side="left", fill="both", expand=True, padx=10)
        doctor_button.pack(side="left", fill="both", expand=True, padx=10)
        admin_button.pack(side="left", fill="both", expand=True, padx=10)
        self.pack_propagate(False)
        
    def patient_login(self):
        pass

    def nurse_login(self):
        pass

    def doctor_login(self):
        pass

    def admin_login(self):
        pass
