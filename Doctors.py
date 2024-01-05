import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class DoctorsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        self.login_label = ttk.Label(self, text="Doctor Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.doctor_id_var = tk.StringVar()
        self.doctor_password_var = tk.StringVar()
        ttk.Label(self, text="Doctor ID:").pack()
        ttk.Entry(self, textvariable=self.doctor_id_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.doctor_password_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.doctor_login).pack(pady=10)
        self.functional_frame = tk.Frame(self)

    def doctor_login(self):
        doctor_id = self.doctor_id_var.get()
        password = self.doctor_password_var.get()
        if self.authenticate_doctor(doctor_id, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.functional_frame.pack(fill="both", expand=True)
            self.load_doctor_functions()
        else:
            messagebox.showerror("Login Failed", "Invalid Doctor ID or password")

    def authenticate_doctor(self, doctor_id, password):
        return True 
    
    def load_doctor_functions(self):
        self.patient_list_label = ttk.Label(self.functional_frame, text="Patients", font=("Arial", 16))
        self.patient_list_label.pack(pady=10)
        self.patient_filter_var = tk.StringVar()
        self.patient_filter_entry = ttk.Entry(self.functional_frame, textvariable=self.patient_filter_var)
        self.patient_filter_entry.pack()
        self.patient_filter_entry.bind("<Return>", self.filter_patients)
        self.patient_listbox = tk.Listbox(self.functional_frame)
        self.patient_listbox.pack(pady=10)
        self.display_patients()
        self.prescription_label = ttk.Label(self.functional_frame, text="Write Prescription", font=("Arial", 16))
        self.prescription_label.pack(pady=10)
        ttk.Label(self.functional_frame, text="Select Patient:").pack()
        self.selected_patient_var = tk.StringVar()
        self.selected_patient_combobox = ttk.Combobox(self.functional_frame, textvariable=self.selected_patient_var, state="readonly")
        self.selected_patient_combobox.pack()
        ttk.Label(self.functional_frame, text="Prescription:").pack()
        self.prescription_text = scrolledtext.ScrolledText(self.functional_frame, wrap=tk.WORD, height=5)
        self.prescription_text.pack(pady=10)
        ttk.Button(self.functional_frame, text="Issue Prescription", command=self.issue_prescription).pack()
        self.update_patient_combobox()

    def display_patients(self):
        patients = ['Patient A', 'Patient B', 'Patient C']
        self.patient_listbox.delete(0, tk.END)
        for patient in patients:
            self.patient_listbox.insert(tk.END, patient)

    def filter_patients(self, event):
        filter_text = self.patient_filter_var.get()
        self.display_patients()

    def update_patient_combobox(self):
        patients = ['Patient A', 'Patient B', 'Patient C']
        self.selected_patient_combobox['values'] = patients

    def issue_prescription(self):
        selected_patient = self.selected_patient_combobox.get()
        prescription = self.prescription_text.get("1.0", tk.END).strip()
        if selected_patient and prescription:
            messagebox.showinfo("Prescription Issued", f"Prescription issued to {selected_patient}.")
            self.prescription_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please select a patient and write a prescription.")