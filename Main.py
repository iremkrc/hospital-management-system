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
        self.root.geometry('1000x600')

        # Initialize the sidebar state
        self.sidebar_open = True

        # Define a style
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14))
        style.configure('TLabel', font=('Arial', 12))

        # Create a header
        self.create_header()

        # Create a toggle button for the sidebar
        self.toggle_button = ttk.Button(root, text="✕", command=self.toggle_sidebar)
        self.toggle_button.pack(anchor="nw")

        # Create the sidebar
        self.sidebar_frame = tk.Frame(root, width=200, bg="lightgray", height=500)
        self.sidebar_frame.pack(side="left", fill="y")

        # Create the main area
        self.main_area = tk.Frame(root, bg="blue")
        self.main_area.pack(expand=True, fill="both", side="right")

        # Sidebar buttons and commands
        self.buttons = [
            ("Dashboard", lambda: self.raise_frame(DashboardFrame(self.main_area))),
            ("Patients", lambda: self.raise_frame(PatientsFrame(self.main_area))),
            ("Nurses", lambda: self.raise_frame(NursesFrame(self.main_area))),
            ("Doctors", lambda: self.raise_frame(DoctorsFrame(self.main_area))),
            ("Admin", lambda: self.raise_frame(AdminFrame(self.main_area))) 


        ]
    
        for text, command in self.buttons:
            button = ttk.Button(self.sidebar_frame, text=text, command=command, style='TButton')
            button.pack(fill="x", padx=10, pady=10)


        # Start on the Dashboard frame
        self.current_frame = DashboardFrame(self.main_area)
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
        # Destroy the current frame
        self.current_frame.destroy()

        # Assign the new frame as the current frame
        self.current_frame = new_frame

        # Pack the new frame
        self.current_frame.pack(fill="both", expand=True)
        