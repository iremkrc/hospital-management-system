import tkinter as tk
from tkinter import ttk
from Appointments import AppointmentsFrame
from Dashboard import DashboardFrame
from Nurses import NursesFrame
from Doctors import DoctorsFrame
from Patients import PatientsFrame
from Admin import AdminFrame

class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry('1200x700')

        self.sidebar_open = True

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14))
        style.configure('TLabel', font=('Arial', 12))

        self.create_header()

        self.toggle_button = ttk.Button(root, text="✕", command=self.toggle_sidebar)
        self.toggle_button.pack(anchor="nw")

        self.sidebar_frame = tk.Frame(root, width=200, bg="lightgray", height=500)
        self.sidebar_frame.pack(side="left", fill="y")

        self.main_area = tk.Frame(root, bg="blue")
        self.main_area.pack(expand=True, fill="both", side="right")

        func = [lambda: self.raise_frame(PatientsFrame(self.main_area)), lambda: self.raise_frame(NursesFrame(self.main_area)), lambda: self.raise_frame(DoctorsFrame(self.main_area)), lambda: self.raise_frame(AdminFrame(self.main_area))]

        self.buttons = [
            ("Dashboard", lambda: self.raise_frame(DashboardFrame(self.main_area, func))),
            ("Patients", func[0]),
            ("Nurses", func[1]),
            ("Doctors", func[2]),
            ("Admin", func[3]) 
        ]
    
        for text, command in self.buttons:
            button = ttk.Button(self.sidebar_frame, text=text, command=command, style='TButton')
            button.pack(fill="x", padx=10, pady=10)


        self.current_frame = DashboardFrame(self.main_area, func)
        self.current_frame.pack(fill="both", expand=True)

    def create_header(self):
        header = tk.Label(self.root, text="Hospital Management System", bg="navy", fg="white", font=("Arial", 24))
        header.pack(side="top", fill="x")


    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar_frame.pack_forget()
            self.toggle_button.config(text="☰")
        else:
            self.sidebar_frame.pack(side="left", fill="y")
            self.toggle_button.config(text="✕")
        self.sidebar_open = not self.sidebar_open

    def raise_frame(self, new_frame):
        self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)
        