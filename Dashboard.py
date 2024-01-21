import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardFrame(tk.Frame):
    def __init__(self, master, functions):
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

        
        patient_button = tk.Button(button_frame, text="I'm a Patient", command=functions[0])
        nurse_button = tk.Button(button_frame, text="I'm a Nurse", command=functions[1])
        doctor_button = tk.Button(button_frame, text="I'm a Doctor", command=functions[2])
        admin_button = tk.Button(button_frame, text="I'm an Admin", command=functions[3])
        patient_button.pack(side="left", fill="both", expand=True, padx=10)
        nurse_button.pack(side="left", fill="both", expand=True, padx=10)
        doctor_button.pack(side="left", fill="both", expand=True, padx=10)
        admin_button.pack(side="left", fill="both", expand=True, padx=10)

        self.pack_propagate(False)

