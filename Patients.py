import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class PatientsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        self.setup_login_ui()

    def setup_login_ui(self):
        self.login_label = ttk.Label(self, text="Patient Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.patient_ssn_var = tk.StringVar()
        self.patient_password_var = tk.StringVar()
        ttk.Label(self, text="SSN:").pack()
        ttk.Entry(self, textvariable=self.patient_ssn_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.patient_ssn_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.patient_login).pack(pady=10)

    def patient_login(self):
        patient_ssn = self.patient_ssn_var.get()
        password = self.patient_password_var.get()

        if not patient_ssn or not password:
            messagebox.showerror("Login Failed", "Patient SSN and Password cannot be empty.")
            return

        if self.authenticate_patient(patient_ssn, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Patient SSN or password")

    def authenticate_patient(self, ssn, password):
        return True

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_login_ui(self):
        for widget in self.winfo_children():
            widget.destroy()


    def load_patient_functions(self):
        self.doctor_list_label = ttk.Label(self.functional_frame, text="Doctors", font=("Arial", 16))
        self.doctor_list_label.pack(pady=10)
        self.doctor_listbox = tk.Listbox(self.functional_frame)
        self.doctor_listbox.pack(pady=10)
        self.display_doctors()
        self.appointment_list_label = ttk.Label(self.functional_frame, text="Appointments", font=("Arial", 16))
        self.appointment_list_label.pack(pady=10)
        self.appointment_listbox = tk.Listbox(self.functional_frame)
        self.appointment_listbox.pack(pady=10)
        self.update_patient_combobox()


    def display_prescriptions(self):
        prescriptions = self.get_prescriptions()  
        self.prescriptions_listbox.delete(0, tk.END)
        for prescription in prescriptions:
            self.prescriptions_listbox.insert(tk.END, prescription)

    def get_patient_info(self):
        # Replace with actual data fetching function
        return "Patient Information:\nName: John Doe\nAge: 30\nGender: Male\n"

    def get_prescriptions(self):
        # Replace with actual data fetching function
        return ["Prescription 1", "Prescription 2", "Prescription 3"]

    def go_back(self):
        # Replace with navigation logic to go back to the previous page
        pass

    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="List Doctors", command=self.show_doctors_ui).pack(pady=10)
        ttk.Button(self, text="List Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="List Companions", command=self.show_companion_ui).pack(pady=10)


    def show_doctors_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Doctors", font=("Arial", 16)).pack(pady=10)
        doctor_listbox = tk.Listbox(self)
        doctor_listbox.pack(pady=10)
        self.display_doctors(doctor_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_appointments_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Appointments", font=("Arial", 16)).pack(pady=10)
        appointment_listbox = tk.Listbox(self)
        appointment_listbox.pack(pady=10)
        self.display_appointments(appointment_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def show_companion_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Companions", font=("Arial", 16)).pack(pady=10)
        companion_listbox = tk.Listbox(self)
        companion_listbox.pack(pady=10)
        self.display_appointments(companion_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

